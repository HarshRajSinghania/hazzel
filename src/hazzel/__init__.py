__version__ = "1.5.3"


def _install_no_color():
    from . import ui
    from .color import apply_to_ui

    apply_to_ui(ui)


_install_no_color()
