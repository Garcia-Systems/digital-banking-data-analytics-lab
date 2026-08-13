from harbor_analytics.analysis import (
    completion_rate,
    count_events,
    group_by_channel,
    unique_sessions,
)
from harbor_analytics.dataset import generate_events


def test_stable_event_count() -> None:
    assert len(generate_events()) == 59


def test_unique_sessions() -> None:
    assert unique_sessions(generate_events()) == 12


def test_application_counts_and_rate() -> None:
    events = generate_events()
    starts = count_events(events, "application_started")
    completions = count_events(events, "application_completed")
    assert starts == 10
    assert completions == 7
    assert completion_rate(starts, completions) == 70.0


def test_channel_segmentation() -> None:
    events = generate_events()
    assert unique_sessions(events, "web") == 7
    assert unique_sessions(events, "mobile") == 5
    assert group_by_channel(events, "application_started") == {"web": 6, "mobile": 4}
    assert group_by_channel(events, "application_completed") == {"web": 5, "mobile": 2}


def test_empty_dataset_is_safe() -> None:
    assert unique_sessions([]) == 0
    assert count_events([], "application_started") == 0
    assert group_by_channel([], "application_started") == {}
    assert completion_rate(0, 0) == 0.0
