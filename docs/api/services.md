# Services

Business logic layer providing encryption, decryption, and hashing operations.

## EncryptionService

Handles all encryption operations with support for AES and PGP methods.

### Methods

#### encrypt_text(secret, password, method="aes")

Encrypt text data.

**Parameters:**
- `secret` (str): Text to encrypt
- `password` (str): Password (AES) or recipient email (PGP)
- `method` (str): "aes" or "pgp" (default: "aes")

**Returns:** str - Encrypted data

**Raises:**
- `EncryptionError`: If encryption fails
- `InvalidInputError`: If parameters are invalid

**Example:**
```python
service = EncryptionService()
encrypted = service.encrypt_text("secret", "password123")
```

#### encrypt_file(file_path, password, method="aes", output_path=None)

Encrypt file contents.

**Parameters:**
- `file_path` (str): Path to file to encrypt
- `password` (str): Password (AES) or recipient email (PGP)
- `method` (str): "aes" or "pgp" (default: "aes")
- `output_path` (str): Optional output file path

**Returns:** str - Encrypted data

**Raises:**
- `FileOperationError`: If file cannot be read
- `EncryptionError`: If encryption fails

**Example:**
```python
service = EncryptionService()
encrypted = service.encrypt_file("document.pdf", "password123")
```

#### encrypt_image(image_path, secret, password, method="aes", stego_method="lsb")

Encrypt and hide data in an image.

**Parameters:**
- `image_path` (str): Path to PNG image
- `secret` (str): Data to hide (text or file path)
- `password` (str): Encryption password
- `method` (str): "aes" or "pgp" (default: "aes")
- `stego_method` (str): "lsb" or "dct" (default: "lsb")

**Returns:** bytes - Image with hidden encrypted data

**Example:**
```python
service = EncryptionService()
encrypted_image = service.encrypt_image(
    "image.png",
    "secret message",
    "password123",
    method="aes",
    stego_method="lsb"
)
```

## DecryptionService

Handles all decryption operations with support for AES and PGP methods.

### Methods

#### decrypt_text(data, password, method="aes")

Decrypt text data.

**Parameters:**
- `data` (str): Encrypted text
- `password` (str): Decryption password or passphrase
- `method` (str): "aes" or "pgp" (default: "aes")

**Returns:** str - Decrypted text

**Raises:**
- `DecryptionError`: If decryption fails
- `InvalidInputError`: If password is incorrect

**Example:**
```python
service = DecryptionService()
decrypted = service.decrypt_text(encrypted, "password123")
```

#### decrypt_file(file_path, password, method="aes", output_path=None)

Decrypt file contents.

**Parameters:**
- `file_path` (str): Path to encrypted file
- `password` (str): Decryption password
- `method` (str): "aes" or "pgp" (default: "aes")
- `output_path` (str): Optional output file path

**Returns:** bytes - Decrypted file data

**Raises:**
- `FileOperationError`: If file cannot be read
- `DecryptionError`: If decryption fails

**Example:**
```python
service = DecryptionService()
decrypted = service.decrypt_file("document.enc", "password123")
```

#### decrypt_image(image_path, password, method="aes", stego_method="lsb")

Extract and decrypt hidden data from image.

**Parameters:**
- `image_path` (str): Path to image with hidden data
- `password` (str): Decryption password
- `method` (str): "aes" or "pgp" (default: "aes")
- `stego_method` (str): "lsb" or "dct" (default: "lsb")

**Returns:** str or bytes - Decrypted data

**Example:**
```python
service = DecryptionService()
data = service.decrypt_image("image.png", "password123", stego_method="lsb")
```

## HashingService

Handles cryptographic hashing operations.

### Attributes

#### ALGORITHMS

Dictionary of available hash algorithms and their implementations.

```python
# List supported algorithms
algorithms = HashingService.ALGORITHMS.keys()
# Output: dict_keys(['MD5', 'SHA1', 'SHA224', 'SHA256', ...])
```

### Methods

#### hash_text(text, algorithm)

Hash text data.

**Parameters:**
- `text` (str): Text to hash
- `algorithm` (str): Hash algorithm (case-insensitive)

**Returns:** str - Hex digest

**Raises:**
- `ValueError`: If algorithm not supported

**Example:**
```python
service = HashingService()
hash_result = service.hash_text("data", "SHA256")
print(hash_result)
```

#### hash_file(file_path, algorithm)

Hash file contents.

**Parameters:**
- `file_path` (str): Path to file
- `algorithm` (str): Hash algorithm

**Returns:** str - Hex digest

**Raises:**
- `FileOperationError`: If file cannot be read
- `ValueError`: If algorithm not supported

**Example:**
```python
service = HashingService()
hash_result = service.hash_file("document.pdf", "SHA256")
```

## Usage Examples

### Complete Workflow

```python
from encryptocli.services import (
    EncryptionService,
    DecryptionService,
    HashingService
)

# Initialize services
encryptor = EncryptionService()
decryptor = DecryptionService()
hasher = HashingService()

# Hash a file to verify integrity
original_hash = hasher.hash_file("important.pdf", "SHA256")

# Encrypt the file
encrypted_data = encryptor.encrypt_file(
    "important.pdf",
    "strong_password_123",
    method="aes"
)

# Later: decrypt the file
decrypted_data = decryptor.decrypt_file(
    "important.pdf.enc",
    "strong_password_123",
    method="aes"
)

# Verify integrity
new_hash = hasher.hash_file("important.pdf", "SHA256")
assert original_hash == new_hash, "File integrity check failed"
```

### Error Handling

```python
from encryptocli.util.exceptions import (
    EncryptionError,
    InvalidInputError
)
from encryptocli.services import EncryptionService

encryptor = EncryptionService()

try:
    encrypted = encryptor.encrypt_text("secret", "password")
except InvalidInputError as e:
    print(f"Invalid input: {e}")
except EncryptionError as e:
    print(f"Encryption failed: {e}")
```
