"""Interfaces module for TUI and CLI handlers."""

from encryptocli.interfaces.tui_handler import TUIHandler


def get_app():
    """Get the Typer application instance (lazy import to avoid hard dependency).

    Returns:
        typer.Typer: The CLI application
    """
    from encryptocli.interfaces.cli_handler import get_app as _get_app

    return _get_app()


__all__ = ["TUIHandler", "get_app"]
