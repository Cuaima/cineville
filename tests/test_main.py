from types import SimpleNamespace

from src.main import main


def test_main_returns_one_for_missing_input_file(monkeypatch) -> None:
    def fake_parse_args() -> SimpleNamespace:
        return SimpleNamespace(
            members="missing-members.csv",
            visits="missing-visits.csv",
            output="result.csv",
        )

    monkeypatch.setattr("src.main.parse_args", fake_parse_args)
    monkeypatch.setattr("src.main.configure_logging", lambda: None)

    assert main() == 1
