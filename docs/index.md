# EncryptoCLI Documentation

Welcome to the EncryptoCLI documentation! EncryptoCLI is a command-line tool that provides an intuitive interface for encrypting, decrypting, and hashing files and text data.

## Features

✨ **Multiple Interfaces**
- Interactive TUI with InquirerPy prompts
- Argument-based CLI using Typer
- Reusable service layer for integration

🔐 **Encryption & Decryption**
- Fernet-based encryption using cryptography
- Password-protected data encryption
- Support for text and file encryption
- LSB steganography for hiding data in images

🔑 **Hashing**
- Multiple hashing algorithms: MD5, SHA256, SHA512, BLAKE2, BLAKE2b
- Support for text and file hashing
- Efficient chunked file processing

🖼️ **Steganography**
- Hide encrypted data within images using LSB method
- Extract hidden data from images
- Powered by the stegano library

## Quick Start

### Interactive Mode (TUI)
```bash
# Install EncryptoCLI
uv pip install encryptocli

# Run interactively
encryptocli
```

### Command-Line Mode (CLI)
```bash
# Hash text
encryptocli hash --text "hello" --algorithm SHA256

# Encrypt text
encryptocli encrypt --text "secret" --password "mypass"

# Decrypt text
encryptocli decrypt --text "encrypted_text" --password "mypass"
```

### As a Library
```python
from encryptocli.services import HashingService

hasher = HashingService()
result = hasher.hash_text("hello", "SHA256")
```

## Architecture

EncryptoCLI is built with **clean separation of concerns**:

- **Services** - Pure business logic (UI-independent)
  - `EncryptionService`
  - `DecryptionService`
  - `HashingService`

- **Interfaces** - UI handlers
  - `TUIHandler` - Interactive prompts
  - `CLIHandler` - Command-line arguments

This architecture enables:
- ✅ Reusable services for any Python project
- ✅ Multiple UI options (TUI, CLI, Web API, etc.)
- ✅ Easy testing without UI dependencies
- ✅ Clean separation of concerns

## What You Can Do

### Hash Data
Generate cryptographic hashes of your data using various algorithms.

### Encrypt Text
Encrypt text and output it as encrypted text or hide it in an image.

### Encrypt Files
Secure your files with password-based encryption (output as `.encrypto` files).

### Decrypt Data
Decrypt encrypted text, files, or data hidden in images using your password.

## Technology Stack

- **Python 3.10+**
- **Cryptography Module** - Fernet encryption
- **InquirerPy** - Interactive CLI prompts
- **Typer** - Command-line arguments
- **Termcolor** - Colored terminal output
- **Stegano** - Image steganography
- **Scrypt** - Key derivation

## Navigation

- **[Getting Started](user-guide/getting-started.md)** - Installation and basic setup
- **[User Guide](user-guide/getting-started.md)** - Detailed guides for each feature
- **[API Reference](api/main.md)** - Complete API documentation
- **[Contributing](contributing.md)** - How to contribute to the project

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
