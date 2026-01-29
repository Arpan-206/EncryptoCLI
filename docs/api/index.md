# API Reference

Developer documentation for EncryptoCLI's core modules and classes.

## Core Modules

- [Services](services.md) - Business logic for encryption, decryption, and hashing
- [Encryption](encryption/index.md) - AES and PGP cipher implementations
- [Interfaces](interfaces/index.md) - CLI and TUI handlers
- [Steganography](steganography/index.md) - LSB and DCT steganography handlers
- [Utilities](utilities/index.md) - Helper functions and exceptions

## Quick Start for Developers

### Import Core Services

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

# Use them
encrypted = encryptor.encrypt_text("secret", "password")
decrypted = decryptor.decrypt_text(encrypted, "password")
hash_result = hasher.hash_text("data", "SHA256")
```

### Use AES Cipher Directly

```python
from encryptocli.encryption.aes import AESCipher

cipher = AESCipher()
encrypted = cipher.encrypt("secret", "password")
decrypted = cipher.decrypt(encrypted, "password")
```

### Use PGP Cipher

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()
encrypted = cipher.encrypt("secret", "recipient@example.com")
decrypted = cipher.decrypt(encrypted)  # Uses default private key
```

### Hash Data

```python
from encryptocli.services import HashingService

hasher = HashingService()

# Hash text
text_hash = hasher.hash_text("data", "SHA256")

# Hash file
file_hash = hasher.hash_file("path/to/file", "SHA256")

# List supported algorithms
algorithms = hasher.ALGORITHMS.keys()
```

## Module Organization

```
encryptocli/
  __init__.py           - Package initialization
  main.py               - CLI/TUI entry point
  error_handler.py      - Error handling
  
  services/             - Business logic
    encryption_service.py
    decryption_service.py
    hashing_service.py
  
  encryption/           - Cipher implementations
    aes/
      cipher.py
    pgp/
      cipher.py
  
  interfaces/           - User interfaces
    cli_handler.py      - Command-line interface
    tui_handler.py      - Text user interface
  
  steganography/        - Data hiding
    lsb/
      handler.py        - LSB steganography
    dct/
      handler.py        - DCT steganography
  
  util/                 - Utilities
    exceptions.py       - Custom exceptions
    file_handling.py    - File operations
    key_gen.py          - Key generation
```

## Error Handling

All modules use custom exceptions from `encryptocli.util.exceptions`:

```python
from encryptocli.util.exceptions import (
    EncryptionError,
    DecryptionError,
    FileOperationError,
    InvalidInputError
)

try:
    encrypted = encryptor.encrypt_text("secret", "password")
except EncryptionError as e:
    print(f"Encryption failed: {e}")
except InvalidInputError as e:
    print(f"Invalid input: {e}")
```

## Version and Metadata

```python
import encryptocli

print(encryptocli.__version__)   # Current version
print(encryptocli.__author__)    # Author name
print(encryptocli.__license__)   # MIT
```

## Next Steps

- [Services](services.md) - Detailed service documentation
- [Encryption](encryption/index.md) - Cipher implementations
- [Steganography](steganography/index.md) - Image data hiding
