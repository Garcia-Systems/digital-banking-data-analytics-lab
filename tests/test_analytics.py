import pytest
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
    assert len(generate_events()) == 1021


def test_unique_sessions() -> None:
    assert unique_sessions(generate_events()) == 189


def test_application_counts_and_rate() -> None:
    events = generate_events()
    starts = count_events(events, "application_started")
    completions = count_events(events, "application_completed")
    assert starts == 168
    assert completions == 148
    assert completion_rate(starts, completions) == pytest.approx(88.0952)


def test_channel_segmentation() -> None:
    events = generate_events()
    assert unique_sessions(events, "web") == 94
    assert unique_sessions(events, "mobile") == 95
    assert group_by_channel(events, "application_started") == {"web": 83, "mobile": 85}
    assert group_by_channel(events, "application_completed") == {"web": 78, "mobile": 70}


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
    assert len(mobile_starts) == 85
    assert group_count(mobile_starts, "channel") == {"mobile": 85}
    assert rate(2, 4) == 50.0
    assert average([2, 4, 6]) == 4.0
    assert average_duration(filter_events(events, "application_completed")) == 1100.0
    assert group_count(events, "source_system") == {
        "member_web": 83,
        "account_opening": 475,
        "identity_provider": 336,
        "mobile_app": 85,
        "harbor_api": 42,
    }
    filter_events,
    group_count,
    rate,
