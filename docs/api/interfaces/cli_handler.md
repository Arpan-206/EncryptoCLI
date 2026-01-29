# CLI Handler

Command-line interface using Click framework.

## Overview

The CLI handler provides command-line access to all EncryptoCLI operations.

```bash
encryptocli --help
```

## Main Commands

### Global Options

- `--help` - Show help message
- `--version` - Show version

### hash

Hash files or text.

```bash
encryptocli hash [OPTIONS]
```

**Options:**
- `--text TEXT` - Text to hash
- `--file FILE` - File path to hash
- `--algorithm ALGO` - Hash algorithm (default: SHA256)
  - MD5, SHA1, SHA224, SHA256, SHA384, SHA512
  - SHA3_224, SHA3_256, SHA3_384, SHA3_512
  - BLAKE2S, BLAKE2B, BLAKE3

**Examples:**
```bash
# Hash text
encryptocli hash --text "hello world" --algorithm SHA256

# Hash file with SHA512
encryptocli hash --file document.pdf --algorithm SHA512

# Hash file with default algorithm
encryptocli hash --file data.txt
```

### encrypt

Encrypt text or files.

```bash
encryptocli encrypt [OPTIONS]
```

**Options:**
- `--text TEXT` - Text to encrypt
- `--file FILE` - File path to encrypt
- `--password PASSWORD` - Encryption password (AES) or recipient email (PGP)
- `--method METHOD` - Encryption method (default: aes)
  - aes: Symmetric encryption
  - pgp: Asymmetric encryption
- `--output FILE` - Output file path (optional)

**Examples:**
```bash
# Encrypt text with AES
encryptocli encrypt --text "secret message" --password "pass123" --method aes

# Encrypt file with PGP
encryptocli encrypt --file document.pdf --password "alice@example.com" --method pgp

# Save to specific output file
encryptocli encrypt --file data.txt --password "pass123" --output encrypted.enc
```

### decrypt

Decrypt text or files.

```bash
encryptocli decrypt [OPTIONS]
```

**Options:**
- `--text TEXT` - Encrypted text to decrypt
- `--file FILE` - Encrypted file path
- `--password PASSWORD` - Decryption password or passphrase
- `--method METHOD` - Decryption method (default: aes)
  - aes: Symmetric decryption
  - pgp: Asymmetric decryption
- `--output FILE` - Output file path (optional)

**Examples:**
```bash
# Decrypt text with AES
encryptocli decrypt --text "encrypted_data" --password "pass123" --method aes

# Decrypt file
encryptocli decrypt --file encrypted.enc --password "pass123"

# Decrypt with PGP
encryptocli decrypt --file document.enc --method pgp

# Save decrypted output to file
encryptocli decrypt --file encrypted.enc --password "pass123" --output decrypted.txt
```

### stego-encrypt

Hide encrypted data in image.

```bash
encryptocli stego-encrypt [OPTIONS]
```

**Options:**
- `--image FILE` - Path to PNG image
- `--secret TEXT` - Data to hide
- `--password PASSWORD` - Encryption password
- `--method METHOD` - Encryption method (default: aes)
- `--stego-method METHOD` - Steganography method (default: lsb)
  - lsb: Least Significant Bit
  - dct: Discrete Cosine Transform

**Examples:**
```bash
# Hide text in image with LSB
encryptocli stego-encrypt --image picture.png --secret "hidden message" --password "pass123" --stego-method lsb

# Hide with DCT method
encryptocli stego-encrypt --image photo.png --secret "secret" --password "pass123" --stego-method dct
```

### stego-decrypt

Extract and decrypt hidden data from image.

```bash
encryptocli stego-decrypt [OPTIONS]
```

**Options:**
- `--image FILE` - Path to image with hidden data
- `--password PASSWORD` - Decryption password
- `--method METHOD` - Encryption method (default: aes)
- `--stego-method METHOD` - Steganography method (default: lsb)

**Examples:**
```bash
# Extract hidden text with LSB
encryptocli stego-decrypt --image picture.png --password "pass123" --stego-method lsb

# Extract with DCT
encryptocli stego-decrypt --image photo.png --password "pass123" --stego-method dct
```

## Common Workflows

### Encrypt and Hash a File

```bash
# Create hash of original
encryptocli hash --file important.pdf --algorithm SHA256 > hash.txt

# Encrypt the file
encryptocli encrypt --file important.pdf --password "secure_pass" --output important.enc

# Later: verify and decrypt
encryptocli decrypt --file important.enc --password "secure_pass" --output important_restored.pdf
encryptocli hash --file important_restored.pdf --algorithm SHA256
```

### Encrypt for Multiple Recipients

```bash
# Encrypt for Alice
encryptocli encrypt --text "message" --password "alice@example.com" --method pgp

# Encrypt for Bob
encryptocli encrypt --text "message" --password "bob@example.com" --method pgp
```

### Create Steganographic Backup

```bash
# Hide encrypted backup in image
encryptocli stego-encrypt --image backup.png --secret "secret_key=xyz123" --password "backup_pass"

# Recover later
encryptocli stego-decrypt --image backup.png --password "backup_pass"
```

## Error Handling

CLI provides clear error messages:

```bash
# Missing required argument
$ encryptocli encrypt --text "secret"
Error: Missing option '--password' / '-p'

# Invalid file path
$ encryptocli hash --file nonexistent.txt
Error: File not found: nonexistent.txt

# Wrong password
$ encryptocli decrypt --file data.enc --password "wrong"
Error: Decryption failed: invalid password
```

## Exit Codes

- `0` - Success
- `1` - Invalid argument
- `2` - File not found
- `3` - Encryption/Decryption error
- `4` - Invalid input

## Tips and Tricks

### Pipe Data

```bash
# Pipe text to encrypt
echo "secret message" | encryptocli encrypt --password "pass123"

# Read from file and encrypt
cat document.txt | encryptocli encrypt --password "pass123"
```

### Use in Scripts

```bash
#!/bin/bash

FILE="backup.tar.gz"
PASSWORD="secure_password"

# Encrypt backup
encryptocli encrypt --file "$FILE" --password "$PASSWORD" --output "$FILE.enc"

# Verify with hash
HASH=$(encryptocli hash --file "$FILE" --algorithm SHA256)
echo "Original hash: $HASH" >> backup_info.txt

# Archive
tar -czf encrypted_backup.tar.gz "$FILE.enc" backup_info.txt
```

### Batch Processing

```bash
#!/bin/bash

# Encrypt all PDFs in directory
for file in *.pdf; do
    encryptocli encrypt --file "$file" --password "pass123" --output "$file.enc"
done

# Hash all files
for file in *; do
    if [ -f "$file" ]; then
        encryptocli hash --file "$file" --algorithm SHA256 >> hashes.txt
    fi
done
```

## See Also

- [TUI Handler](tui_handler.md)
- [Services Documentation](../services.md)
- [User Guide](../../user-guide/index.md)
