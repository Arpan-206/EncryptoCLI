# EncryptoCLI Documentation

Welcome to the EncryptoCLI documentation! EncryptoCLI is a command-line program that provides an intuitive and easy-to-use interface for encrypting, decrypting, and hashing files and text data.

## Features

✨ **Encryption & Decryption**
- Fernet-based encryption using cryptography
- Password-protected data encryption
- Support for text and file encryption
- LSB steganography for hiding data in images

🔐 **Hashing**
- Multiple hashing algorithms: MD5, SHA256, SHA512, BLAKE2, BLAKE2b
- Support for text and file hashing
- Efficient chunked file processing

🖼️ **Steganography**
- Hide encrypted data within images using LSB method
- Extract hidden data from images
- Powered by the stegano library

## Quick Start

```bash
# Install EncryptoCLI
uv pip install encryptocli

# Run the CLI
python main.py
```

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
- **Termcolor** - Colored terminal output
- **InquirerPy** - Interactive CLI prompts
- **Stegano** - Image steganography
- **Scrypt** - Key derivation

## Navigation

- **[Getting Started](user-guide/getting-started.md)** - Installation and basic setup
- **[User Guide](user-guide/getting-started.md)** - Detailed guides for each feature
- **[API Reference](api/main.md)** - Complete API documentation
- **[Contributing](contributing.md)** - How to contribute to the project

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
