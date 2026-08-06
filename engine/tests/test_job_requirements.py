from __future__ import annotations

from ats_engine.contracts import ProcessStatus
from ats_engine.job_requirements import extract_job_requirements


def test_extracts_tr_en_spans_categories_modality_and_negation():
    text = (
        "İleri düzey İngilizce zorunludur. "
        "En az 3 yıl dış ticaret deneyimi gereklidir. "
        "SAP bilgisi tercih sebebidir. "
        "Almanca zorunlu değildir. "
        "Şirketimiz 1998 yılında kurulmuştur."
    )
    result = extract_job_requirements("JOB-1", text)

    assert result.review_required is True
    assert len(result.requirements) == 4
    assert [item.modality for item in result.requirements] == [
        "MUST",
        "MUST",
        "PREFERRED",
        "MUST",
    ]
    assert [item.category for item in result.requirements] == [
        "LANGUAGE",
        "EXPERIENCE",
        "SKILL",
        "LANGUAGE",
    ]
    assert result.requirements[3].negated is True
    assert all(item.review_status is ProcessStatus.REVIEW for item in result.requirements)
    assert all(text[item.span_start : item.span_end] == item.text for item in result.requirements)


def test_does_not_promote_arbitrary_body_keywords_to_must_have():
    text = "SAP ERP Incoterms gümrük lojistik. Şirketimiz global pazarlarda faaliyet gösterir."
    result = extract_job_requirements("JOB-2", text)
    assert result.requirements == []
    assert result.review_required is False


def test_requirement_ids_are_stable_for_same_snapshot_text():
    text = "Bachelor degree is required. English is preferred."
    first = extract_job_requirements("JOB-3", text)
    second = extract_job_requirements("JOB-3", text)
    assert [item.id for item in first.requirements] == [item.id for item in second.requirements]
    assert first.source_sha256 == second.source_sha256
