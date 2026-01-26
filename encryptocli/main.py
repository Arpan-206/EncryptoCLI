"""CLI entrypoint for EncryptoCLI using TUI handler."""

from encryptocli.interfaces.tui_handler import TUIHandler


def main() -> None:
    """Legacy entrypoint retained for backward compatibility.

    Runs the TUI interface.

    Returns:
        None
    """
    tui = TUIHandler()
    tui.run()


if __name__ == "__main__":
    main()
