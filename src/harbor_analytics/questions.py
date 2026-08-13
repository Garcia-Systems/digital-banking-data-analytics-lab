"""Educational analytical-question specifications and evidence checks."""

from dataclasses import dataclass
from collections.abc import Iterable, Mapping


QUESTION_TYPES = {"descriptive", "diagnostic", "causal", "predictive"}


@dataclass(frozen=True)
class AnalyticalQuestion:
    name: str
    population: str
    outcome: str
    dimensions: tuple[str, ...]
    comparison: str | None
    question_type: str
    required_fields: frozenset[str]
    required_evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.question_type not in QUESTION_TYPES:
            raise ValueError(f"Unknown question type: {self.question_type}")


@dataclass(frozen=True)
class EvidenceReadiness:
    answerable: bool
    missing_fields: tuple[str, ...]
    missing_evidence: tuple[str, ...]


def available_fields(events: Iterable[Mapping[str, object]]) -> set[str]:
    """Return fields present on every event; empty data supplies no fields."""
    rows = list(events)
    return set.intersection(*(set(row) for row in rows)) if rows else set()


def assess_evidence(
    question: AnalyticalQuestion, events: Iterable[Mapping[str, object]]
) -> EvidenceReadiness:
    """Check schema fields and explicitly identified evidence unavailable here."""
    missing_fields = tuple(sorted(question.required_fields - available_fields(events)))
    missing_evidence = question.required_evidence
    return EvidenceReadiness(not missing_fields and not missing_evidence, missing_fields, missing_evidence)


HARBOR_QUESTIONS = (
    AnalyticalQuestion("How many applications started?", "observed account-opening sessions", "application_started", (), None, "descriptive", frozenset({"event_name", "session_id"})),
    AnalyticalQuestion("What is completion rate by channel?", "observed account-opening sessions", "application_completed", ("channel",), "mobile compared with web", "descriptive", frozenset({"channel", "event_name", "session_id"})),
    AnalyticalQuestion("At which recorded stage is abandonment highest?", "observed account-opening sessions", "stage progression", ("page_or_feature",), "successive recorded stages", "diagnostic", frozenset({"event_name", "page_or_feature", "session_id"})),
    AnalyticalQuestion("Did the identity-verification provider cause lower mobile conversion?", "mobile account-opening sessions", "application_completed", ("channel", "source_system"), "provider exposure", "causal", frozenset({"channel", "event_name", "source_system", "session_id"}), ("randomized or credible comparison assignment", "provider/version exposure identity", "confounder controls")),
    AnalyticalQuestion("Which members are most likely to abandon next month?", "future account-opening members", "future abandonment", ("anonymous_or_synthetic_member_id",), None, "predictive", frozenset({"anonymous_or_synthetic_member_id", "event_name"}), ("labeled historical outcomes across time", "prediction features available before outcome", "out-of-sample validation")),
)
