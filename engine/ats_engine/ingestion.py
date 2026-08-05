"""Binary document ingestion with explicit unsupported/OCR states."""

from __future__ import annotations

import hashlib
import mimetypes
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from .contracts import DocumentParseResult, ProcessStatus
from .errors import DocumentParseError, ErrorCode, InvalidInputError

_WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _artifact_id(path: Path, data: bytes) -> str:
    return f"artifact-{hashlib.sha256(data).hexdigest()[:16]}"


def _xml_text(data: bytes) -> str:
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise DocumentParseError(f"DOCX XML ayrıştırılamadı: {exc}") from exc

    lines: list[str] = []
    for paragraph in root.iter(f"{_WORD_NS}p"):
        parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{_WORD_NS}t" and node.text:
                parts.append(node.text)
            elif node.tag == f"{_WORD_NS}tab":
                parts.append("\t")
            elif node.tag == f"{_WORD_NS}br":
                parts.append("\n")
        text = "".join(parts).strip()
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
        ordered_parts.extend(sorted(name for name in names if name.startswith("word/header") and name.endswith(".xml")))
        ordered_parts.extend(sorted(name for name in names if name.startswith("word/footer") and name.endswith(".xml")))
        ordered_parts.extend(
            name for name in ("word/footnotes.xml", "word/endnotes.xml", "word/comments.xml") if name in names
        )
        chunks = [_xml_text(archive.read(name)) for name in ordered_parts if name in names]

    text = "\n\n".join(chunk for chunk in chunks if chunk).strip()
    if not text:
        raise DocumentParseError("DOCX içinde çıkarılabilir metin bulunamadı.", code=ErrorCode.EMPTY_DOCUMENT)
    return DocumentParseResult(
        artifact_id=_artifact_id(source, data),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        text=text,
        status=ProcessStatus.PASS,
        extraction_method="docx-ooxml-full-story",
    )


def parse_pdf(path: str | Path) -> DocumentParseResult:
    source = Path(path)
    data = source.read_bytes()
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency is in base install
        raise DocumentParseError("PDF ingestion için pypdf kurulmalıdır.", code=ErrorCode.UNSUPPORTED_FORMAT) from exc

    try:
        reader = PdfReader(source)
        page_texts = [(page.extract_text() or "").strip() for page in reader.pages]
    except Exception as exc:
        raise DocumentParseError(f"PDF ayrıştırılamadı: {type(exc).__name__}: {exc}") from exc

    if not page_texts or not any(page_texts):
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
        extraction_method="pypdf-text-layer",
    )


def parse_document(path: str | Path) -> DocumentParseResult:
    source = Path(path)
    if not source.is_file():
        raise InvalidInputError(f"Belge bulunamadı: {source}", field="path")
    suffix = source.suffix.lower()
    if suffix == ".docx":
        return parse_docx(source)
    if suffix == ".pdf":
        return parse_pdf(source)
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
