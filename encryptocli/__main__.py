"""Module entry point for EncryptoCLI.

This allows the package to be run as a module:
    python -m encryptocli              # Run interactive TUI
    python -m encryptocli encrypt --help  # Run CLI with arguments
"""

import sys

from encryptocli.interfaces.tui_handler import TUIHandler


def main() -> None:
    """Entry point that determines whether to use TUI or CLI interface.

    If no arguments are provided, runs the interactive TUI.
    If arguments are provided, uses the argument-based CLI (typer).

    Returns:
        None
    """
    # If no arguments beyond the module name, run interactive TUI
    if len(sys.argv) == 1:
        tui = TUIHandler()
        tui.run()
    else:
        # Import typer CLI lazily - only needed for CLI mode
        try:
            from encryptocli.interfaces.cli_handler import get_app

            app = get_app()
            app()
        except ImportError as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
