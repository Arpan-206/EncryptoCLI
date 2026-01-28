# EncryptoCLI Documentation

Welcome to the EncryptoCLI documentation! **Secure CLI for hashing, encryption, and steganography (AES/Fernet and PGP).**

## Features

✨ **Multiple Interfaces**
- Interactive TUI with InquirerPy prompts
- Argument-based CLI using Typer
- Reusable service layer for integration

🔐 **Encryption & Decryption**
- **AES/Fernet encryption** - Fast symmetric encryption with password-based key derivation
- **PGP encryption** - Asymmetric encryption with public/private key pairs (RSA 2048-bit)
- Password-protected data encryption
- Support for text and file encryption
- LSB and DCT steganography for hiding data in images

🔑 **Hashing**
- **14 hashing algorithms**: MD5, SHA1, SHA-2 family (SHA224/256/384/512), SHA-3 family (SHA3_224/256/384/512), BLAKE2S/B, BLAKE3
- Support for text and file hashing
- Efficient chunked file processing for large files

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

# Encrypt text with AES
encryptocli encrypt --text "secret" --password "mypass" --method aes

# Encrypt text with PGP
encryptocli encrypt --text "secret" --password "recipient@example.com" --method pgp

# Decrypt text
encryptocli decrypt --text "encrypted_text" --password "mypass" --method aes

# PGP key management
encryptocli pgp-key gen     # Generate key pair
encryptocli pgp-key list    # List keys
encryptocli pgp-key export  # Export public key
encryptocli pgp-key import  # Import public key
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
