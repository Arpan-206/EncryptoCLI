# Utilities

Helper modules and utility functions.

## Overview

Utilities package provides common functionality used across EncryptoCLI:

- Custom exceptions
- File handling operations
- Cryptographic key generation

## Exceptions

Custom exception classes for error handling.

```python
from encryptocli.util.exceptions import (
    EncryptionError,
    DecryptionError,
    FileOperationError,
    InvalidInputError
)
```

See [Exceptions Documentation](exceptions.md) for complete reference.

## File Handling

File I/O and path operations.

```python
from encryptocli.util.file_handling import (
    read_file,
    write_file,
    validate_path,
    get_file_size
)
```

See [File Handling Documentation](file_handling.md) for complete reference.

## Key Generation

Cryptographic key derivation and management.

```python
from encryptocli.util.key_gen import (
    derive_key,
    generate_salt,
    generate_iv
)
```

See [Key Generation Documentation](key_gen.md) for complete reference.

## Module Contents

- **exceptions.py** - Custom exception classes
- **file_handling.py** - File operations
- **key_gen.py** - Key derivation

## Usage Examples

### Error Handling

```python
from encryptocli.util.exceptions import DecryptionError
from encryptocli.services import DecryptionService

service = DecryptionService()

try:
    result = service.decrypt_text(encrypted, "wrong_password")
except DecryptionError as e:
    print(f"Decryption failed: {e}")
```

### File Operations

```python
from encryptocli.util.file_handling import read_file, write_file

# Read file
content = read_file("document.txt")

# Process content
encrypted = encrypt(content)

# Write file
write_file("document.enc", encrypted)
```

### Key Operations

```python
from encryptocli.util.key_gen import derive_key, generate_salt

# Generate salt for key derivation
salt = generate_salt()

# Derive encryption key from password
key = derive_key("password", salt)
```

## See Also

- [Exceptions](exceptions.md)
- [File Handling](file_handling.md)
- [Key Generation](key_gen.md)
- [Services](../services.md)
