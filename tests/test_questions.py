import pytest

from harbor_analytics.dataset import generate_events
from harbor_analytics.questions import AnalyticalQuestion, HARBOR_QUESTIONS, assess_evidence, available_fields


def test_question_classification_and_validation() -> None:
    assert [question.question_type for question in HARBOR_QUESTIONS] == [
        "descriptive", "descriptive", "diagnostic", "causal", "predictive"
    ]
    with pytest.raises(ValueError):
        AnalyticalQuestion("bad", "all", "x", (), None, "guess", frozenset())


def test_answerable_and_unsupported_questions() -> None:
    results = [assess_evidence(question, generate_events()) for question in HARBOR_QUESTIONS]
    assert [result.answerable for result in results] == [True, True, True, False, False]
    assert "confounder controls" in results[3].missing_evidence


def test_required_field_detection_and_empty_input() -> None:
    question = HARBOR_QUESTIONS[1]
    incomplete = [{"event_name": "application_started", "session_id": "one"}]
    assert assess_evidence(question, incomplete).missing_fields == ("channel",)
    assert available_fields([]) == set()
    assert assess_evidence(question, []).missing_fields == ("channel", "event_name", "session_id")
