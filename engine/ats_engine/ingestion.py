"""Binary document ingestion with explicit unsupported/OCR states."""

from __future__ import annotations

import hashlib
import mimetypes
import zipfile
from collections.abc import Callable
from pathlib import Path
from xml.etree import ElementTree

from .contracts import DocumentParseResult, ProcessStatus
from .errors import DocumentParseError, ErrorCode, InvalidInputError

_WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
OCRAdapter = Callable[[Path], str]


def _artifact_id(path: Path, data: bytes) -> str:
    return f"artifact-{hashlib.sha256(data).hexdigest()[:16]}"


def _paragraph_text(paragraph: ElementTree.Element) -> str:
    """Extract one paragraph without consuming text from nested paragraphs.

    Word text boxes are commonly represented as ``w:p`` elements nested inside
    an outer drawing paragraph. Walking the outer paragraph recursively and then
    walking every nested paragraph again duplicates the text and can concatenate
    separate text-box lines without separators. Nested paragraphs are therefore
    left for the document-level paragraph iterator to process exactly once.
    """
    parts: list[str] = []

    def walk(node: ElementTree.Element) -> None:
        for child in node:
            if child.tag == f"{_WORD_NS}p":
                continue
            if child.tag == f"{_WORD_NS}t" and child.text:
                parts.append(child.text)
            elif child.tag == f"{_WORD_NS}tab":
                parts.append("\t")
            elif child.tag == f"{_WORD_NS}br":
                parts.append("\n")
            walk(child)

    walk(paragraph)
    return "".join(parts).strip()


def _xml_text(data: bytes) -> str:
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise DocumentParseError(f"DOCX XML ayrıştırılamadı: {exc}") from exc

    lines: list[str] = []
    for paragraph in root.iter(f"{_WORD_NS}p"):
        text = _paragraph_text(paragraph)
        if text:
            lines.append(text)
    return "\n".join(lines)


def parse_docx(path: str | Path) -> DocumentParseResult:
    source = Path(path)
    data = source.read_bytes()
    if not zipfile.is_zipfile(source):
        raise DocumentParseError("Geçersiz DOCX ZIP paketi.")

    ordered_parts = ["word/document.xml"]
    with zipfile.ZipFile(source) as archive:
        names = set(archive.namelist())
        headers = sorted(name for name in names if name.startswith("word/header") and name.endswith(".xml"))
        footers = sorted(name for name in names if name.startswith("word/footer") and name.endswith(".xml"))
        ordered_parts.extend(headers)
        ordered_parts.extend(footers)
        ordered_parts.extend(
            name for name in ("word/footnotes.xml", "word/endnotes.xml", "word/comments.xml") if name in names
        )
        part_bytes = {name: archive.read(name) for name in ordered_parts if name in names}
        chunks = [_xml_text(part_bytes[name]) for name in ordered_parts if name in part_bytes]
        document_xml = part_bytes.get("word/document.xml", b"")
        try:
            document_root = ElementTree.fromstring(document_xml)
        except ElementTree.ParseError as exc:
            raise DocumentParseError(f"DOCX document.xml ayrıştırılamadı: {exc}") from exc
        structural_features = {
            "paragraph_count": len(list(document_root.iter(f"{_WORD_NS}p"))),
            "table_count": len(list(document_root.iter(f"{_WORD_NS}tbl"))),
            "text_box_count": len(list(document_root.iter(f"{_WORD_NS}txbxContent"))),
            "header_part_count": len(headers),
            "footer_part_count": len(footers),
            "section_count": len(list(document_root.iter(f"{_WORD_NS}sectPr"))),
        }

    text = "\n\n".join(chunk for chunk in chunks if chunk).strip()
    if not text:
        raise DocumentParseError("DOCX içinde çıkarılabilir metin bulunamadı.", code=ErrorCode.EMPTY_DOCUMENT)
    return DocumentParseResult(
        artifact_id=_artifact_id(source, data),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        text=text,
        status=ProcessStatus.PASS,
        extraction_method="docx-ooxml-full-story",
        structural_features=structural_features,
    )


def parse_pdf(path: str | Path, *, ocr_adapter: OCRAdapter | None = None) -> DocumentParseResult:
    source = Path(path)
    data = source.read_bytes()
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency is in base install
        raise DocumentParseError("PDF ingestion için pypdf kurulmalıdır.", code=ErrorCode.UNSUPPORTED_FORMAT) from exc

    try:
        reader = PdfReader(source)
        page_texts = []
        extraction_modes = []
        for page in reader.pages:
            try:
                extracted = page.extract_text(extraction_mode="layout") or ""
                extraction_modes.append("layout")
            except (TypeError, ValueError, KeyError):
                try:
                    extracted = page.extract_text() or ""
                    extraction_modes.append("plain")
                except KeyError:
                    extracted = ""
                    extraction_modes.append("no-content-stream")
            page_texts.append(extracted.strip())
    except Exception as exc:
        raise DocumentParseError(f"PDF ayrıştırılamadı: {type(exc).__name__}: {exc}") from exc

    if not page_texts or not any(page_texts):
        if ocr_adapter is not None:
            try:
                ocr_text = ocr_adapter(source).strip()
            except Exception as exc:
                raise DocumentParseError(f"OCR adaptörü başarısız: {type(exc).__name__}: {exc}") from exc
            if not ocr_text:
                raise DocumentParseError("OCR adaptörü metin üretmedi.", code=ErrorCode.EMPTY_DOCUMENT)
            return DocumentParseResult(
                artifact_id=_artifact_id(source, data),
                media_type="application/pdf",
                text=ocr_text,
                status=ProcessStatus.REVIEW,
                warnings=["OCR çıktısı insan doğrulaması gerektirir."],
                page_count=len(page_texts),
                extraction_method="optional-ocr-adapter",
                structural_features={"text_layer_pages": 0, "ocr_required": True},
                page_evidence=[
                    {"page": index + 1, "text_characters": 0, "method": "ocr-document-level"}
                    for index in range(len(page_texts))
                ],
            )
        raise DocumentParseError(
            "PDF text layer içermiyor; OCR adaptörü gerekli.",
            code=ErrorCode.SCANNED_PDF_REQUIRES_OCR,
        )
    empty_pages = [str(index + 1) for index, text in enumerate(page_texts) if not text]
    warnings = []
    status = ProcessStatus.PASS
    if empty_pages:
        status = ProcessStatus.REVIEW
        warnings.append("Metinsiz sayfalar tespit edildi (olası mixed/scanned PDF): " + ", ".join(empty_pages))
    return DocumentParseResult(
        artifact_id=_artifact_id(source, data),
        media_type="application/pdf",
        text="\n\n".join(page_texts).strip(),
        status=status,
        warnings=warnings,
        page_count=len(page_texts),
        extraction_method="pypdf-layout-text-layer"
        if all(mode == "layout" for mode in extraction_modes)
        else "pypdf-text-layer",
        structural_features={
            "text_layer_pages": sum(bool(text) for text in page_texts),
            "empty_pages": [int(page) for page in empty_pages],
            "reading_order_verified": False,
        },
        page_evidence=[
            {"page": index + 1, "text_characters": len(text), "method": extraction_modes[index]}
            for index, text in enumerate(page_texts)
        ],
    )


def parse_document(path: str | Path, *, ocr_adapter: OCRAdapter | None = None) -> DocumentParseResult:
    source = Path(path)
    if not source.is_file():
        raise InvalidInputError(f"Belge bulunamadı: {source}", field="path")
    suffix = source.suffix.lower()
    if suffix == ".docx":
        return parse_docx(source)
    if suffix == ".pdf":
        return parse_pdf(source, ocr_adapter=ocr_adapter)
    if suffix in {".txt", ".md"}:
        data = source.read_bytes()
        text = data.decode("utf-8").strip()
        if not text:
            raise DocumentParseError("Metin belgesi boş.", code=ErrorCode.EMPTY_DOCUMENT)
        return DocumentParseResult(
            artifact_id=_artifact_id(source, data),
            media_type=mimetypes.guess_type(source.name)[0] or "text/plain",
            text=text,
            status=ProcessStatus.PASS,
            extraction_method="utf-8-text",
        )
    raise DocumentParseError(
        f"Desteklenmeyen belge türü: {suffix or '<uzantısız>'}",
        code=ErrorCode.UNSUPPORTED_FORMAT,
    )
