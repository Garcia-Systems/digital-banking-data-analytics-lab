from pathlib import Path

from harbor_analytics.analysis import load_events
from harbor_analytics.dataset import generate_events, write_events

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "synthetic" / "digital_events.csv"


def test_generation_is_deterministic() -> None:
    assert generate_events() == generate_events()


def test_generated_fixture_is_byte_for_byte_stable(tmp_path: Path) -> None:
    generated = tmp_path / "events.csv"
    write_events(generated)
    assert generated.read_bytes() == FIXTURE.read_bytes()


def test_fixture_loads_generated_events() -> None:
    assert load_events(FIXTURE) == generate_events()

