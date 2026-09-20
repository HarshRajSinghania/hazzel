import io
import os

from hazzel import ui


def test_env_no_color_present_and_nonempty(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert ui.env_no_color() is True
    monkeypatch.setenv("NO_COLOR", "true")
    assert ui.env_no_color() is True


def test_env_no_color_absent_or_empty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    assert ui.env_no_color() is False
    monkeypatch.setenv("NO_COLOR", "")
    assert ui.env_no_color() is False


def test_no_color_disables_output(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    buf = io.StringIO()
    console = ui.make_console(file=buf, width=80, force_terminal=True)
    console.print("[bold red]hi[/bold red]")
    output = buf.getvalue()
    assert "hi" in output
    assert "\x1b" not in output


def test_color_remains_when_no_color_unset(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    buf = io.StringIO()
    console = ui.make_console(file=buf, width=80, force_terminal=True)
    console.print("[bold red]hi[/bold red]")
    output = buf.getvalue()
    assert "hi" in output
    assert "\x1b" in output


def test_context_meter_plain_when_no_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    text = ui.format_context_meter(100, 1_000_000)
    assert "\x1b" not in text
    assert ui.format_context_plain(100, 1_000_000) == text
