# Encryption

Cipher implementations for AES and PGP encryption.

## Overview

EncryptoCLI provides two primary encryption methods:

1. **AES (Fernet)** - Symmetric encryption
2. **PGP** - Asymmetric encryption

## AES Cipher

Implements Fernet authenticated encryption using passwords.

### Usage

```python
from encryptocli.encryption.aes import AESCipher

cipher = AESCipher()

# Encrypt text
encrypted = cipher.encrypt("secret message", "password123")

# Decrypt text
decrypted = cipher.decrypt(encrypted, "password123")
print(decrypted)  # Output: "secret message"
```

### Methods

#### encrypt(plaintext, password)

Encrypt plaintext using password.

**Parameters:**
- `plaintext` (str): Text to encrypt
- `password` (str): Encryption password

**Returns:** str - Encrypted text

#### decrypt(ciphertext, password)

Decrypt ciphertext using password.

**Parameters:**
- `ciphertext` (str): Encrypted text
- `password` (str): Decryption password

**Returns:** str - Decrypted plaintext

**Raises:** 
- `DecryptionError` - Wrong password or corrupted data

### Security

- Uses Fernet (symmetric authenticated encryption)
- Based on AES-128 in CBC mode
- Includes HMAC for authentication
- 16-byte salt per encryption

## PGP Cipher

Implements PGP encryption using GNU Privacy Guard.

### Requirements

- GPG installed on system
- Public/private key pair configured

### Usage

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()

# Encrypt for recipient
encrypted = cipher.encrypt("secret", "recipient@example.com")

# Decrypt with private key
decrypted = cipher.decrypt(encrypted)
```

### Methods

#### encrypt(plaintext, recipient_email)

Encrypt plaintext for recipient using their public key.

**Parameters:**
- `plaintext` (str): Text to encrypt
- `recipient_email` (str): Recipient's email address

**Returns:** str - Encrypted text (PGP armored format)

#### decrypt(ciphertext, passphrase=None)

Decrypt ciphertext using private key.

**Parameters:**
- `ciphertext` (str): Encrypted text
- `passphrase` (str): Private key passphrase (optional)

**Returns:** str - Decrypted plaintext

**Raises:**
- `DecryptionError` - Wrong passphrase or no matching key

### Key Management

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()

# List available keys
keys = cipher.list_keys()
for key in keys:
    print(f"{key['name']} <{key['email']}>")

# List secret keys
secret_keys = cipher.list_secret_keys()
```

## Comparison

| Feature | AES | PGP |
|---------|-----|-----|
| Encryption Type | Symmetric | Asymmetric |
| Key Type | Password | Key pair |
| Setup | None | Key generation required |
| Security | Good | Excellent |
| Speed | Fast | Slower |
| Use Case | Personal files | Secure communication |

## Implementation Details

### AES Implementation

- **Algorithm**: Fernet (AES-128-CBC)
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **IV**: 16 random bytes per encryption
- **Authentication**: HMAC-SHA256

### PGP Implementation

- **Algorithm**: RSA (typical)
- **Key Size**: 2048-4096 bits (user dependent)
- **Format**: Armored (ASCII-safe)
- **Backend**: GNU Privacy Guard (gpg)

## See Also

- [AES Cipher Documentation](aes_cipher.md)
- [PGP Cipher Documentation](pgp.md)
- [Services - High-level API](../services.md)
