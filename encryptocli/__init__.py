"""EncryptoCLI - A command-line tool for encryption, decryption, and hashing.

A powerful and intuitive CLI application for:
- Encrypting and decrypting files and text using Fernet encryption
- Generating cryptographic hashes with multiple algorithms
- Hiding encrypted data in images using LSB steganography
"""

__version__ = "0.2.2"
__author__ = "Arpan Pandey"
__license__ = "MIT"

from encryptocli.main import EncryptoCLI, main

__all__ = ["EncryptoCLI", "main", "__version__", "__author__", "__license__"]
