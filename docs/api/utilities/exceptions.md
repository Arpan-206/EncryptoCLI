# Exceptions

Custom exception classes for EncryptoCLI error handling.

## Exception Hierarchy

```
Exception
├── EncryptoCLIException (base class)
│   ├── EncryptionError
│   ├── DecryptionError
│   ├── FileOperationError
│   └── InvalidInputError
```

## Base Exception

### EncryptoCLIException

Base exception for all EncryptoCLI errors.

```python
from encryptocli.util.exceptions import EncryptoCLIException

try:
    # Some operation
    pass
except EncryptoCLIException as e:
    # Catches any EncryptoCLI error
    print(f"Error: {e}")
```

## Specific Exceptions

### EncryptionError

Raised when encryption operation fails.

**Causes:**
- Invalid plaintext
- Invalid password/key
- Cipher initialization failure
- Unsupported encryption method
- File permission issues

**Example:**
```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.util.exceptions import EncryptionError

cipher = AESCipher()

try:
    encrypted = cipher.encrypt(plaintext, password)
except EncryptionError as e:
    print(f"Encryption failed: {e}")
```

### DecryptionError

Raised when decryption operation fails.

**Causes:**
- Wrong password
- Corrupted ciphertext
- Invalid cipher format
- Unsupported decryption method
- Key not found (PGP)

**Example:**
```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.util.exceptions import DecryptionError

cipher = AESCipher()

try:
    decrypted = cipher.decrypt(ciphertext, password)
except DecryptionError as e:
    print(f"Decryption failed: {e}")
    if "password" in str(e).lower():
        print("Try with correct password")
```

### FileOperationError

Raised when file I/O operations fail.

**Causes:**
- File not found
- Permission denied
- Directory not found
- Disk full
- File read/write failure
- Invalid file path

**Example:**
```python
from encryptocli.services import EncryptionService
from encryptocli.util.exceptions import FileOperationError

service = EncryptionService()

try:
    encrypted = service.encrypt_file("/path/to/file.txt", "password")
except FileOperationError as e:
    print(f"File operation failed: {e}")
    if "not found" in str(e).lower():
        print("File does not exist")
    elif "permission" in str(e).lower():
        print("Permission denied - check file permissions")
```

### InvalidInputError

Raised when input validation fails.

**Causes:**
- Empty input
- Invalid format
- Unsupported algorithm
- Invalid email address
- Data too large
- Missing required parameters

**Example:**
```python
from encryptocli.services import HashingService
from encryptocli.util.exceptions import InvalidInputError

service = HashingService()

try:
    hash_result = service.hash_text(data, "INVALID_ALGORITHM")
except InvalidInputError as e:
    print(f"Invalid input: {e}")
    print(f"Supported algorithms: {service.ALGORITHMS.keys()}")
```

## Error Handling Patterns

### Basic Try-Except

```python
from encryptocli.services import EncryptionService
from encryptocli.util.exceptions import (
    EncryptionError,
    InvalidInputError
)

service = EncryptionService()

try:
    result = service.encrypt_text(secret, password)
except EncryptionError as e:
    print(f"Encryption error: {e}")
except InvalidInputError as e:
    print(f"Invalid input: {e}")
```

### Catch All EncryptoCLI Errors

```python
from encryptocli.services import EncryptionService
from encryptocli.util.exceptions import EncryptoCLIException

service = EncryptionService()

try:
    result = service.encrypt_file(path, password)
except EncryptoCLIException as e:
    print(f"EncryptoCLI error: {e}")
    # Handle any EncryptoCLI error
```

### Multi-Level Error Handling

```python
from encryptocli.services import DecryptionService
from encryptocli.util.exceptions import (
    DecryptionError,
    FileOperationError,
    EncryptoCLIException
)

service = DecryptionService()

try:
    result = service.decrypt_file(encrypted_path, password)
except FileOperationError as e:
    print(f"Cannot read file: {e}")
except DecryptionError as e:
    print(f"Wrong password or corrupted data: {e}")
except EncryptoCLIException as e:
    print(f"Other error: {e}")
```

### With Cleanup

```python
from encryptocli.services import EncryptionService
from encryptocli.util.exceptions import EncryptoCLIException
import tempfile

service = EncryptionService()
temp_file = None

try:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    encrypted = service.encrypt_file(source, password)
    temp_file.write(encrypted)
    print("Encryption successful")
except EncryptoCLIException as e:
    print(f"Error: {e}")
finally:
    if temp_file:
        temp_file.close()
        # Optional: clean up temp file
```

## Exception Messages

Exception messages are descriptive and actionable:

```python
try:
    # Missing file
    encrypt_file("missing.txt", "password")
except FileOperationError as e:
    # e.message: "File not found: missing.txt"
    print(e)
```

## Best Practices

### 1. Specific Exception Handling

Good:
```python
try:
    decrypt_text(data, password)
except DecryptionError as e:
    print("Wrong password")
```

Bad:
```python
try:
    decrypt_text(data, password)
except Exception as e:
    print("Something went wrong")
```

### 2. Log Exception Information

```python
import logging
from encryptocli.util.exceptions import EncryptoCLIException

logger = logging.getLogger(__name__)

try:
    operation()
except EncryptoCLIException as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
```

### 3. Provide Context

```python
try:
    encrypted = service.encrypt_file(path, password)
except FileOperationError as e:
    print(f"Cannot encrypt {path}: {e}")
except Exception as e:
    print(f"Encryption failed: {e}")
```

### 4. Retry Logic

```python
from encryptocli.util.exceptions import DecryptionError

def decrypt_with_retry(data, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            password = input("Enter password: ")
            return decrypt_text(data, password)
        except DecryptionError:
            if attempt < max_attempts - 1:
                print("Wrong password, try again")
            else:
                print("Failed - wrong password")
                raise
```

## See Also

- [Services](../services.md)
- [File Handling](file_handling.md)
- [Key Generation](key_gen.md)
