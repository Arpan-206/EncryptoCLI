# PGP Cipher API Reference

## Overview

The `PGPCipher` class provides a complete interface for PGP/GPG encryption and decryption operations. It uses the `python-gnupg` library to wrap GPG functionality.

## Class: PGPCipher

```python
from encryptocli.encryption.pgp import PGPCipher

pgp = PGPCipher()
```

### Constructor

```python
def __init__(self) -> None
```

**Description**: Initializes a new PGP cipher instance with an isolated GPG home directory.

**Returns**: None

**Example**:
```python
pgp = PGPCipher()
# Temporary GPG home created at self.gnupg_home
```

---

## Methods

### generate_key_pair

```python
def generate_key_pair(
    self,
    name: str,
    email: str,
    passphrase: str
) -> str
```

**Description**: Generate a new PGP key pair (RSA 2048-bit).

**Parameters**:
- `name` (str): Full name for the key
- `email` (str): Email address for the key
- `passphrase` (str): Passphrase to protect the private key

**Returns**: str - Key fingerprint

**Raises**: 
- `FatalError` - If required parameters are missing or key generation fails

**Example**:
```python
fingerprint = pgp.generate_key_pair(
    name="Alice Smith",
    email="alice@example.com",
    passphrase="my_secure_passphrase"
)
print(f"Generated key: {fingerprint}")
```

---

### encrypt_text

```python
def encrypt_text(
    self,
    secret: str,
    recipient_email: str,
    passphrase: Optional[str] = None
) -> str
```

**Description**: Encrypt plain text using the recipient's public key.

**Parameters**:
- `secret` (str): Plain text to encrypt
- `recipient_email` (str): Recipient's email address (must have public key in keyring)
- `passphrase` (Optional[str]): Optional passphrase for signing the message (not implemented by default)

**Returns**: str - Encrypted ciphertext in PGP format

**Raises**:
- `FatalError` - If encryption fails or recipient key not found

**Example**:
```python
encrypted = pgp.encrypt_text(
    secret="This is confidential",
    recipient_email="alice@example.com"
)
print(encrypted)  # PGP-encrypted message
```

---

### decrypt_text

```python
def decrypt_text(
    self,
    encrypted_secret: str,
    passphrase: str
) -> str
```

**Description**: Decrypt PGP-encrypted text using the private key.

**Parameters**:
- `encrypted_secret` (str): PGP-encrypted ciphertext
- `passphrase` (str): Passphrase for the private key

**Returns**: str - Decrypted plaintext

**Raises**:
- `FatalError` - If passphrase is empty or decryption fails

**Example**:
```python
decrypted = pgp.decrypt_text(
    encrypted_secret=encrypted,
    passphrase="my_secure_passphrase"
)
print(decrypted)  # "This is confidential"
```

---

### encrypt_file

```python
def encrypt_file(
    self,
    file_path: str,
    recipient_email: str
) -> str
```

**Description**: Encrypt a file using the recipient's public key. Creates a `.pgp` file.

**Parameters**:
- `file_path` (str): Path to the file to encrypt
- `recipient_email` (str): Recipient's email address

**Returns**: str - Success message

**Raises**:
- `FatalError` - If file encryption fails
- `MildError` - If file is already encrypted (`.pgp` or `.gpg` extension)

**Example**:
```python
result = pgp.encrypt_file(
    file_path="document.pdf",
    recipient_email="alice@example.com"
)
print(result)  # "File encrypted successfully"
# Creates: document.pdf.pgp
```

---

### decrypt_file

```python
def decrypt_file(
    self,
    file_path: str,
    passphrase: str,
    output_dir: str = "./"
) -> str
```

**Description**: Decrypt a PGP-encrypted file. Creates `decrypted_<filename>` in the output directory.

**Parameters**:
- `file_path` (str): Path to the encrypted file
- `passphrase` (str): Passphrase for the private key
- `output_dir` (str, optional): Output directory for decrypted file (default: "./")

**Returns**: str - Success message with output path

**Raises**:
- `FatalError` - If passphrase is empty or decryption fails

**Example**:
```python
result = pgp.decrypt_file(
    file_path="document.pdf.pgp",
    passphrase="my_secure_passphrase",
    output_dir="./decrypted/"
)
print(result)  # "File decrypted successfully to ./decrypted/decrypted_document.pdf"
```

---

### export_public_key

```python
def export_public_key(
    self,
    email: str,
    output_path: str
) -> str
```

**Description**: Export a public key to a file for sharing with others.

**Parameters**:
- `email` (str): Email address of the key to export
- `output_path` (str): Path where the public key will be saved (typically `.asc`)

**Returns**: str - Success message

**Raises**:
- `FatalError` - If export fails or key not found

**Example**:
```python
result = pgp.export_public_key(
    email="alice@example.com",
    output_path="alice_public.asc"
)
print(result)  # "Public key exported to alice_public.asc"
```

---

### import_public_key

```python
def import_public_key(
    self,
    key_path: str
) -> str
```

**Description**: Import a public key from a file into the keyring.

**Parameters**:
- `key_path` (str): Path to the public key file (`.asc` format)

**Returns**: str - Success message with key fingerprint

**Raises**:
- `FatalError` - If import fails

**Example**:
```python
result = pgp.import_public_key(
    key_path="alice_public.asc"
)
print(result)  # "Public key imported successfully. Fingerprint: ABC123..."
```

---

### list_keys

```python
def list_keys(self) -> list
```

**Description**: List all available keys in the keyring.

**Returns**: list - List of key information dictionaries

**Raises**:
- `FatalError` - If key listing fails

**Example**:
```python
keys = pgp.list_keys()
for key in keys:
    print(f"Email: {key.get('uids', [''])[0]}")
    print(f"Fingerprint: {key['keyid']}")
    print(f"Type: {key['type']}")
```

Key dictionary structure:
```python
{
    'keyid': '1234567890ABCDEF',
    'type': 'pub',
    'uids': ['Alice Smith <alice@example.com>'],
    'expires': '0',
    'length': '2048',
    'algo': '1',  # RSA
    'fingerprint': '1234567890ABCDEF1234567890ABCDEF12345678'
}
```

---

## Exception Handling

### FatalError

Raised for critical encryption/decryption errors:

```python
from encryptocli.util.exceptions import FatalError

try:
    pgp.encrypt_text("message", "user@example.com")
except FatalError as e:
    print(f"Encryption failed: {e}")
```

### MildError

Raised for non-critical issues (e.g., file already encrypted):

```python
from encryptocli.util.exceptions import MildError

try:
    pgp.encrypt_file("document.pgp", "user@example.com")
except MildError as e:
    print(f"Warning: {e}")
```

---

## Complete Usage Example

```python
from encryptocli.encryption.pgp import PGPCipher

# Initialize
pgp = PGPCipher()

# Step 1: Generate key pair for yourself
my_fingerprint = pgp.generate_key_pair(
    name="John Doe",
    email="john@example.com",
    passphrase="my_passphrase123"
)
print(f"My key: {my_fingerprint}")

# Step 2: Generate key pair for recipient (or import theirs)
recipient_fingerprint = pgp.generate_key_pair(
    name="Alice Smith",
    email="alice@example.com",
    passphrase="alice_passphrase456"
)

# Step 3: Encrypt a message for Alice
message = "This is a secret message"
encrypted = pgp.encrypt_text(message, "alice@example.com")
print(f"Encrypted: {encrypted[:50]}...")

# Step 4: Alice decrypts the message
decrypted = pgp.decrypt_text(encrypted, "alice_passphrase456")
print(f"Decrypted: {decrypted}")

# Step 5: Encrypt a file for Alice
encrypted_file = pgp.encrypt_file("report.pdf", "alice@example.com")
print(encrypted_file)

# Step 6: Export public key for sharing
pgp.export_public_key("john@example.com", "john_public.asc")

# Step 7: List all keys
keys = pgp.list_keys()
for key in keys:
    print(f"Key: {key['uids']}")
```

---

## Integration with Services

Use PGP through the service layer:

```python
from encryptocli.services import EncryptionService, DecryptionService

# Create services
encryption_service = EncryptionService()
decryption_service = DecryptionService()

# Encrypt with PGP method
encrypted = encryption_service.encrypt_text(
    secret="Sensitive data",
    password="recipient@example.com",
    method="pgp"
)

# Decrypt with PGP method
decrypted = decryption_service.decrypt_text(
    data=encrypted,
    password="your_passphrase",
    method="pgp"
)

# Encrypt file with PGP
encryption_service.encrypt_file(
    file_path="document.pdf",
    password="recipient@example.com",
    method="pgp"
)

# Decrypt file with PGP
decryption_service.decrypt_file(
    file_path="document.pdf.pgp",
    password="your_passphrase",
    method="pgp",
    output_dir="./"
)
```

---

## Performance Characteristics

- **Key Generation**: ~5-10 seconds (2048-bit RSA)
- **Text Encryption**: Milliseconds to seconds depending on message size
- **File Encryption**: Depends on file size (typically fast)
- **Decryption**: Slightly slower than encryption

---

## Security Notes

1. **Key Storage**: Keys stored in temporary directory (isolated per instance)
2. **Passphrase**: Never hardcode or log passphrases
3. **Key Trust**: Uses `always_trust=True` for convenience (override for production)
4. **Message Signing**: Not enabled by default
5. **Key Backup**: Export and securely backup important keys

---

## See Also

- [Parent Module Documentation](../api/encryption/pgp.md)
- [User Guide - PGP](../user-guide/pgp.md)
- [python-gnupg Documentation](https://python-gnupg.readthedocs.io/)
