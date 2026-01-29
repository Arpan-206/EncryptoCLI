# EncryptoCLI Documentation

!!! note "AI-Generated Documentation"
    This documentation was written entirely by AI. While we strive for accuracy, please verify critical information against the source code and report any discrepancies.

EncryptoCLI is a powerful command-line tool for encryption, decryption, hashing, and image steganography. It provides both a CLI and TUI (Text User Interface) for easy interaction.

## Core Features

- **Encryption**: AES (Fernet) and PGP encryption methods
- **Decryption**: Support for both AES and PGP encrypted data
- **Hashing**: Multiple cryptographic hash algorithms (MD5, SHA256, SHA512, BLAKE2, BLAKE3, etc.)
- **Steganography**: Hide encrypted data in images using LSB or DCT methods

## Quick Links

- [Getting Started](getting-started.md) - Installation and first steps
- [User Guide](user-guide/index.md) - Detailed usage instructions
- [API Reference](api/index.md) - Developer documentation

## Interfaces

EncryptoCLI offers two ways to interact with the system:

- **CLI Mode**: Command-line interface for scripting and automation
- **TUI Mode**: Interactive text user interface for manual operations

Simply run `encryptocli` without arguments to launch the TUI, or provide command arguments for CLI mode.
