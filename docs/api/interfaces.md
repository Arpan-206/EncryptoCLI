# Interfaces

EncryptoCLI provides multiple interfaces to interact with the core services.

## Interface Overview

The application supports two primary interfaces:

- **TUI Handler** - Interactive prompts-based interface for human users
- **CLI Handler** - Argument-based command-line interface for scripting and automation

Both interfaces use the same underlying service layer, ensuring consistency and reusability.

## TUI Handler

::: encryptocli.interfaces.tui_handler.TUIHandler

Interactive interface using InquirerPy for prompts. Best for manual user interaction.

## CLI Handler

::: encryptocli.interfaces.cli_handler.get_app

Argument-based interface using Typer for command-line arguments. Best for scripting and automation.
