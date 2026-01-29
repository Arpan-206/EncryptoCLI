# User Guide

Comprehensive guides for using EncryptoCLI features.

## Operations

- [Hashing](hashing.md) - Generate cryptographic hashes
- [Encryption](encryption.md) - Protect your data with encryption
- [Decryption](decryption.md) - Recover encrypted data
- [Steganography](steganography.md) - Hide data in images
- [PGP Key Management](pgp-key-management.md) - Manage PGP keys

## Common Tasks

### Encrypt a File

1. Run `encryptocli` in TUI mode
2. Select "Encrypt" operation
3. Choose "File" as data type
4. Enter the file path
5. Select encryption method (AES or PGP)
6. Provide password or recipient email
7. Save the encrypted output

### Decrypt a File

1. Run `encryptocli` in TUI mode
2. Select "Decrypt" operation
3. Choose "File" as data type
4. Enter the encrypted file path
5. Select decryption method
6. Provide password or passphrase
7. Save the decrypted output

### Hash a File

1. Run `encryptocli` in TUI mode
2. Select "Hash" operation
3. Choose "File" as data type
4. Enter the file path
5. Select hash algorithm
6. View and copy the hash result

## Supported Formats

- **Text**: Plain text input directly in the interface
- **Files**: Any file type can be encrypted, decrypted, or hashed
- **Images**: PNG images for steganography operations
