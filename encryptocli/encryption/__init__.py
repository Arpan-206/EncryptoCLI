"""Encryption module for EncryptoCLI.

Provides encryption and decryption functionality using Fernet encryption.
"""

from encryptocli.encryption.aes.cipher import AESCipher

__all__ = ["AESCipher"]
