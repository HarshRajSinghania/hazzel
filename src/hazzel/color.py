"""NO_COLOR handling for Hazzel's shared Rich console.

https://no-color.org/ — when NO_COLOR is present and non-empty, styled
output is disabled. Rich's ``no_color`` flag still emits bold/dim SGR
codes, so we also drop the color system.
"""

import os

from rich.console import Console


def env_no_color():
    """True when NO_COLOR is set and non-empty."""
    value = os.environ.get("NO_COLOR")
    return value is not None and value != ""


def make_console(**kwargs):
    if env_no_color():
        kwargs.setdefault("no_color", True)
        kwargs.setdefault("color_system", None)
        kwargs.setdefault("highlight", False)
    return Console(**kwargs)


def apply_to_ui(ui_module):
    """Attach helpers onto ``hazzel.ui`` and honor NO_COLOR."""
    ui_module.env_no_color = env_no_color
    ui_module.make_console = make_console
    if env_no_color():
        ui_module.console = make_console()
    _orig_meter = ui_module.format_context_meter

    def format_context_meter(used, window):
        if env_no_color():
            return ui_module.format_context_plain(used, window)
        return _orig_meter(used, window)

    ui_module.format_context_meter = format_context_meter
