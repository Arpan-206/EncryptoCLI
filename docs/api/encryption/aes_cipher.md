# AES Cipher

Symmetric encryption using Fernet (AES-128-CBC).

## Class: AESCipher

```python
from encryptocli.encryption.aes import AESCipher

cipher = AESCipher()
```

## Methods

### encrypt(plaintext, password)

Encrypt plaintext using AES-128-CBC with password derivation.

**Parameters:**
- `plaintext` (str): Text to encrypt
- `password` (str): Encryption password (any length)

**Returns:** str - Base64-encoded encrypted data

**Raises:**
- `EncryptionError` - If encryption fails

**Example:**
```python
cipher = AESCipher()
encrypted = cipher.encrypt("sensitive data", "my_password")
print(encrypted)
```

### decrypt(ciphertext, password)

Decrypt ciphertext using provided password.

**Parameters:**
- `ciphertext` (str): Base64-encoded encrypted data
- `password` (str): Decryption password

**Returns:** str - Decrypted plaintext

**Raises:**
- `DecryptionError` - If password is wrong or data is corrupted
- `InvalidInputError` - If ciphertext format is invalid

**Example:**
```python
cipher = AESCipher()
try:
    decrypted = cipher.decrypt(encrypted, "my_password")
except DecryptionError:
    print("Wrong password")
```

## Security Details

### Key Derivation

- Algorithm: PBKDF2
- Hash: SHA-256
- Iterations: 100,000
- Salt: 16 random bytes

### Encryption

- Algorithm: AES-128 in CBC mode
- Block Size: 128 bits (16 bytes)
- IV: 16 random bytes per encryption
- Padding: PKCS7

### Authentication

- HMAC-SHA256 for authentication
- Prevents tampering detection

### Output Format

Encrypted output is base64-encoded for safe transmission:

```
base64(salt + iv + ciphertext + hmac)
```

## Password Security

### Password Requirements

- **Minimum**: 6 characters
- **Recommended**: 12+ characters
- **Strong**: Mix uppercase, lowercase, numbers, symbols

### Password Quality

- Longer passwords are more secure
- Use unique passwords for different data
- Avoid dictionary words
- Avoid personal information

### Password Storage

- Never hardcode passwords in source code
- Use environment variables or secure vaults
- Never commit passwords to version control

## Usage Examples

### Encrypt and Decrypt Text

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.util.exceptions import DecryptionError

cipher = AESCipher()

# Encrypt
plaintext = "This is a secret message"
password = "secure_password_123"
encrypted = cipher.encrypt(plaintext, password)
print(f"Encrypted: {encrypted[:50]}...")

# Decrypt
try:
    decrypted = cipher.decrypt(encrypted, password)
    print(f"Decrypted: {decrypted}")
except DecryptionError:
    print("Decryption failed - wrong password or corrupted data")
```

### Encrypt File Contents

```python
from encryptocli.encryption.aes import AESCipher

cipher = AESCipher()

# Read file
with open("document.txt", "r") as f:
    content = f.read()

# Encrypt
encrypted = cipher.encrypt(content, "password123")

# Save encrypted
with open("document.enc", "w") as f:
    f.write(encrypted)
```

### Decrypt File

```python
from encryptocli.encryption.aes import AESCipher

cipher = AESCipher()

# Read encrypted file
with open("document.enc", "r") as f:
    encrypted = f.read()

# Decrypt
decrypted = cipher.decrypt(encrypted, "password123")

# Save decrypted
with open("document.txt", "w") as f:
    f.write(decrypted)
```

## Error Handling

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.util.exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidInputError
)

cipher = AESCipher()

try:
    encrypted = cipher.encrypt("data", "password")
except EncryptionError as e:
    print(f"Encryption error: {e}")

try:
    decrypted = cipher.decrypt(encrypted, "wrong_password")
except DecryptionError as e:
    print(f"Decryption failed: {e}")
except InvalidInputError as e:
    print(f"Invalid data format: {e}")
```

## Performance

- Works efficiently with typical data sizes
- Key derivation involves intentional computation delay for security

## Compatibility

- Works with any text-based data
- Output is portable across platforms
- Encrypted data can be transmitted via email, chat, etc.
- Recipient needs same AESCipher class to decrypt

## Limitations

- Symmetric encryption (same password to encrypt/decrypt)
- Not suitable for public key distribution
- Password must be remembered or stored securely
- No built-in key management

## Related Classes

- [Services - EncryptionService](../services.md)
- [Utilities - Exceptions](../utilities/exceptions.md)
