# EncryptoCLI

![EncryptoCLI Thumbnail](./docs/EncryptoCLI-Thumbnail.png)

[![PyPI version](https://badge.fury.io/py/EncryptoCLI.svg)](https://badge.fury.io/py/EncryptoCLI)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📚 Description

EncryptoCLI is a powerful command-line tool for encryption, decryption, hashing, and steganography operations. It provides both an interactive TUI (Text User Interface) and a traditional CLI for flexible workflows.

### Key Features

- **Multiple Encryption Methods**: AES (Fernet) and PGP/GPG support
- **13 Hash Algorithms**: MD5, SHA256, SHA512, BLAKE2, BLAKE3, and more
- **Image Steganography**: Hide encrypted data in images using LSB or DCT methods
- **Dual Interfaces**: Interactive TUI or command-line arguments
- **Modern Python**: Built with Python 3.10+ type hints and async support

## 🚀 Installation

```bash
pip install EncryptoCLI
```

### Requirements

- Python 3.10 or higher
- GPG (GNU Privacy Guard) for PGP encryption - [Install GPG](https://gnupg.org/download/)

## 💻 Usage

### Interactive Mode (TUI)

Simply run without arguments to launch the interactive interface:

```bash
encryptocli
```

### Command-Line Mode

#### Hashing

```bash
# Hash text
encryptocli hash --text "secret message" --algorithm SHA256

# Hash file
encryptocli hash --file document.pdf --algorithm SHA512
```

**Supported Algorithms**: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512, BLAKE2b, BLAKE2s, BLAKE3

#### AES Encryption

```bash
# Encrypt text
encryptocli encrypt --text "secret" --password "mypassword" --method aes

# Encrypt file
encryptocli encrypt --file document.txt --password "mypassword" --method aes

# Decrypt
encryptocli decrypt --file document.txt.enc --password "mypassword" --method aes
```

#### PGP Encryption

PGP encryption supports three ways to specify the recipient:

```bash
# Using recipient email (key from GPG keyring)
encryptocli encrypt --text "secret" --recipient-email "user@example.com" --method pgp

# Using public key file
encryptocli encrypt --text "secret" --recipient-key-file ~/recipient-pubkey.asc --method pgp

# Using inline public key
encryptocli encrypt --text "secret" --recipient-key "-----BEGIN PGP PUBLIC KEY BLOCK-----..." --method pgp

# Decrypt (requires your private key passphrase)
encryptocli decrypt --text "encrypted_data" --password "your_passphrase" --method pgp
```

#### Steganography

Hide encrypted data inside images:

```bash
# Encrypt and hide in image
encryptocli encrypt --text "secret" --password "pass" --image cover.png --steganography lsb

# Extract and decrypt from image
encryptocli decrypt --image cover.png --password "pass" --steganography lsb
```

**Steganography Methods**:
- `lsb` - Least Significant Bit (higher capacity)
- `dct` - Discrete Cosine Transform (more robust)




## 🐋 Docker
You can pull this image from Docker Hub and build it very easily.
1. Just pull the image. 
    ```bash
    docker pull arpanpandey/encrypto:latest
    ```
OR 

1. You can build the image using.
    ```bash
    docker build --pull --rm -f "Dockerfile" -t arpanpandey/encrypto:latest "."
    ```

2. Running the container with the image (Be sure to put the `-t` and `-d` flag.)
    ```bash
    docker run -t -d arpanpandey/encrypto:latest
    ```

## License
This project is licensed under the MIT License.

### Video Demo
You can access the video demo at [https://youtu.be/Zmf2EK9jPCw](https://youtu.be/Zmf2EK9jPCw)

### Contributors 🏆🏆

<a href="https://github.com/Arpan-206/EncryptoCLI/graphs/contributors">
<img src="https://contrib.rocks/image?repo=Arpan-206/EncryptoCLI" />

### MY BLOG
https://hackersreboot.tech/

#### Thank You!
Thanks a lot to the team at CS50 for teaching me so much about the fascinating world of computer science and program.


