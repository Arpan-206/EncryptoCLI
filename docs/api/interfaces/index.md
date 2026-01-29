# Interfaces

User interface handlers for CLI and TUI modes.

## Overview

EncryptoCLI provides two interface options:

1. **CLI (Command-Line Interface)** - Argument-based control
2. **TUI (Text User Interface)** - Interactive menu-driven interface

## CLI Handler

Command-line interface using Click framework.

```python
from encryptocli.interfaces.cli_handler import app

# Run the CLI
app()
```

### Usage

```bash
# View help
encryptocli --help

# Hash a file
encryptocli hash --file document.pdf --algorithm SHA256

# Encrypt with AES
encryptocli encrypt --text "secret" --password "pass123" --method aes

# Decrypt
encryptocli decrypt --file encrypted.enc --password "pass123"
```

See [CLI Handler Documentation](cli_handler.md) for detailed command reference.

## TUI Handler

Interactive Text User Interface using InquirerPy.

```python
from encryptocli.interfaces.tui_handler import TUIHandler

# Launch interactive UI
tui = TUIHandler()
tui.run()
```

### Usage

```bash
# Launch interactive mode (no arguments)
encryptocli
```

The TUI presents:
- Main menu with operations
- Contextual prompts
- Real-time validation
- Error messages and guidance

See [TUI Handler Documentation](tui_handler.md) for detailed information.

## Comparison

| Feature | CLI | TUI |
|---------|-----|-----|
| Automation | Excellent | Poor |
| Scripting | Yes | No |
| Learning Curve | Moderate | Low |
| Error Messages | Concise | Detailed |
| Interactive | No | Yes |
| Visual Feedback | Minimal | Rich |

## Choosing an Interface

### Use CLI When:
- Automating tasks
- Creating scripts
- Integrating with other tools
- Working in non-interactive environments
- Need exact control

### Use TUI When:
- First-time user
- Manual operations
- Prefer guided experience
- Want help with decisions
- Testing features

## Integration Example

```python
from encryptocli.main import main

# This automatically routes to appropriate interface
if len(sys.argv) > 1:
    # Use CLI with arguments
    main()
else:
    # Use TUI interactive mode
    main()
```

## Custom Integration

### Using Services Directly

For programmatic access without UI:

```python
from encryptocli.services import (
    EncryptionService,
    DecryptionService,
    HashingService
)

# Bypass UI, use services directly
encryptor = EncryptionService()
encrypted = encryptor.encrypt_text("secret", "password")
```

## See Also

- [CLI Handler Documentation](cli_handler.md)
- [TUI Handler Documentation](tui_handler.md)
- [Services Documentation](../services.md)
