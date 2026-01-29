# Getting Started

## Installation

Install EncryptoCLI using pip:

```bash
pip install encryptocli
```

## Basic Usage

### TUI Mode (Default)

Launch the interactive interface:

```bash
encryptocli
```

This opens the Text User Interface where you can:
- Select operations through interactive menus
- Encrypt and decrypt text or files
- Generate hashes
- Use steganography

### CLI Mode

Use command-line arguments directly:

```bash
encryptocli --help
```

## First Steps

1. **Hashing**: Start with hashing operations - they require no setup
   - Hash text or files
   - Choose from 13 supported algorithms

2. **Encryption**: Encrypt your first file
   - Choose AES for password-based encryption
   - Choose PGP for public key cryptography

3. **Decryption**: Decrypt files using stored keys

4. **Steganography**: Hide encrypted data in images

## Dependencies

EncryptoCLI requires:

- **Python 3.8+**
- **GPG** (GNU Privacy Guard) for PGP operations
  - Install on macOS: `brew install gnupg`
  - Install on Ubuntu/Debian: `sudo apt-get install gnupg`
  - Install on Windows: Download from [gnupg.org](https://www.gnupg.org/download/)

## Verify Installation

```bash
encryptocli --version
```

Should display the installed version of EncryptoCLI.
