"""SYN-002: every SynthesisChange must carry model/prompt attribution metadata.

evidence_ids/reason establish that a change is evidence-bound; they do not
say what produced the wording. A human reviewer needs to know whether a
change was manually authored or LLM-drafted, and by which model/prompt
version, to weigh it appropriately.
"""

from __future__ import annotations

import pytest

from ats_engine.errors import InvalidInputError
from ats_engine.safe_synthesis import apply_change_set, approve_change_set, build_change_set, rollback_change_set


def test_change_defaults_to_honest_human_authored_metadata_not_a_fabricated_model():
    change_set = build_change_set(
        "changes-1",
        [{"path": "cv.summary", "old_value": "old", "new_value": "new", "evidence_ids": ["EV-1"]}],
        known_evidence_ids={"EV-1"},
    )
    change = change_set.changes[0]
    assert change.model_id == "human"
    assert change.prompt_id == "human-authored"
    assert change.model_version and change.prompt_version


def test_change_accepts_explicit_model_and_prompt_attribution():
    change_set = build_change_set(
        "changes-2",
        [
            {
                "path": "cv.summary",
                "old_value": "old",
                "new_value": "new",
                "evidence_ids": ["EV-1"],
                "model_id": "gpt-x",
                "model_version": "2026-08-01",
                "prompt_id": "cv-summary-rewrite",
                "prompt_version": "3",
            }
        ],
        known_evidence_ids={"EV-1"},
    )
    change = change_set.changes[0]
    assert change.model_id == "gpt-x"
    assert change.model_version == "2026-08-01"
    assert change.prompt_id == "cv-summary-rewrite"
    assert change.prompt_version == "3"


def test_change_set_level_defaults_apply_to_every_proposal():
    change_set = build_change_set(
        "changes-3",
        [{"path": "cv.summary", "new_value": "new", "evidence_ids": ["EV-1"]}],
        known_evidence_ids={"EV-1"},
        default_model_id="claude-y",
        default_model_version="2026-08-05",
        default_prompt_id="batch-rewrite",
        default_prompt_version="1",
    )
    change = change_set.changes[0]
    assert change.model_id == "claude-y"
    assert change.prompt_id == "batch-rewrite"


def test_blank_model_attribution_is_rejected():
    with pytest.raises(InvalidInputError):
        build_change_set(
            "changes-4",
            [
                {
                    "path": "cv.summary",
                    "new_value": "new",
                    "evidence_ids": ["EV-1"],
                    "model_id": "   ",
                }
            ],
            known_evidence_ids={"EV-1"},
            default_model_id="   ",
        )


def test_rollback_change_carries_its_own_attribution_not_the_original():
    proposed = build_change_set(
        "changes-5",
        [{"path": "cv.summary", "old_value": "old", "new_value": "new", "evidence_ids": ["EV-1"]}],
        known_evidence_ids={"EV-1"},
    )
    approved = approve_change_set(proposed)
    document, applied = apply_change_set(approved, {"cv.summary": "old"})
    _restored, rollback = rollback_change_set(applied, document, rollback_id="rollback-1")
    rollback_change = rollback.changes[0]
    assert rollback_change.model_id == "system-rollback"
    assert "rollback-of:" in rollback_change.prompt_id
