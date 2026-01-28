"""Entrypoint for EncryptoCLI - routes to CLI or TUI based on arguments."""

import sys
from encryptocli.interfaces.cli_handler import app as cli_app
from encryptocli.interfaces.tui_handler import TUIHandler


def main() -> None:
    """Route to CLI or TUI based on command-line arguments.

    If command-line arguments are provided, use CLI interface.
    Otherwise, launch TUI interface.

    Returns:
        None
    """
    # If arguments are provided (excluding the script name), use CLI
    if len(sys.argv) > 1:
        cli_app()
    else:
        # No arguments, launch TUI
        tui = TUIHandler()
        tui.run()


if __name__ == "__main__":
    main()
