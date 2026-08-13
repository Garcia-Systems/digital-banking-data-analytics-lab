from harbor_analytics.analysis import (
    average,
    average_duration,
    completion_rate,
    count_events,
    filter_events,
    group_count,
    group_by_channel,
    rate,
    unique_sessions,
)
from harbor_analytics.dataset import generate_events


def test_stable_event_count() -> None:
    assert len(generate_events()) == 61


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
    assert filter_events([]) == []
    assert group_count([], "source_system") == {}
    assert rate(3, 0) == 0.0
    assert average([]) == 0.0
    assert average_duration([]) == 0.0


def test_filter_group_rate_average_and_sources() -> None:
    events = generate_events()
    mobile_starts = filter_events(events, "application_started", channel="mobile")
    assert len(mobile_starts) == 4
    assert group_count(mobile_starts, "channel") == {"mobile": 4}
    assert rate(2, 4) == 50.0
    assert average([2, 4, 6]) == 4.0
    assert average_duration(filter_events(events, "application_completed")) == 1100.0
    assert group_count(events, "source_system") == {
        "member_web": 7,
        "account_opening": 25,
        "identity_provider": 20,
        "mobile_app": 4,
        "harbor_api": 3,
        "transfer_service": 2,
    }
    filter_events,
    group_count,
    rate,
