# Hashing Guide

Hashing is a one-way function that converts data into a fixed-size string of characters. It's commonly used for password storage, data integrity verification, and digital signatures.

## Supported Algorithms

EncryptoCLI supports five industry-standard hashing algorithms:

### MD5
- **Speed**: Very Fast
- **Output Size**: 128 bits (32 hex characters)
- **Use Case**: Legacy applications (NOT recommended for security-critical applications)
- **Note**: Cryptographically broken, use only when required for compatibility

### SHA256
- **Speed**: Fast
- **Output Size**: 256 bits (64 hex characters)
- **Use Case**: Recommended for most applications
- **Note**: Part of the SHA-2 family, widely used and trusted

### SHA512
- **Speed**: Fast
- **Output Size**: 512 bits (128 hex characters)
- **Use Case**: When stronger hashing is needed
- **Note**: Provides more resistance to collision attacks

### BLAKE2
- **Speed**: Fastest
- **Output Size**: 256 bits (64 hex characters)
- **Use Case**: Performance-critical applications
- **Note**: Modern algorithm, faster than MD5, SHA-2, and SHA-3

### BLAKE2b
- **Speed**: Fastest
- **Output Size**: 512 bits (128 hex characters)
- **Use Case**: Maximum security with excellent performance
- **Note**: 64-bit version of BLAKE2, recommended for new projects

## How to Hash Data

### Step 1: Select Hashing Operation

From the main menu, select **Hash**:

```
? What do you want to do?
❯ Hash
  Encrypt
  Decrypt
  Exit
```

### Step 2: Choose Algorithm

Select your preferred algorithm:

```
? Which algorithm do you want to use?
❯ MD5
  SHA256
  SHA512
  BLAKE2
  BLAKE2b
```

### Step 3: Choose Data Type

Select whether you want to hash **Text** or a **File**:

```
? What do you want to hash?
❯ Text
  File
```

### Hashing Text

If you selected **Text**:

1. Enter the text to hash:
   ```
   ? Enter data to hash: Hello, World!
   ```

2. View the hash result:
   ```
   Your hash is: <hash_output>
   ```

### Hashing Files

If you selected **File**:

1. Provide the file path:
   ```
   ? Enter the path to the file: /path/to/document.txt
   ```

2. View the hash result:
   ```
   Your hash is: <hash_output>
   ```

## Algorithm Recommendations

| Use Case | Recommended Algorithm |
|----------|----------------------|
| New Projects | BLAKE2b |
| Password Hashing* | Use bcrypt/argon2 instead |
| Checksums | BLAKE2 or SHA256 |
| Compliance Requirements | SHA256 or SHA512 |
| Performance Priority | BLAKE2 |
| Backward Compatibility | SHA256 |

*Note: For password hashing, consider using dedicated algorithms like bcrypt or Argon2, not general-purpose hashing algorithms.

## Use Cases

### File Integrity Verification

Hash a file to create a checksum. Later, hash the same file again to verify it hasn't been modified:

```bash
# Create checksum
$ echo "document.txt" | encryptocli hash
Your hash is: a1b2c3d4e5f6...

# Later, verify the file
$ echo "document.txt" | encryptocli hash
Your hash is: a1b2c3d4e5f6...  # Should match!
```

### Data Integrity in Transfers

Hash data before sending it over insecure channels, then hash the received data to ensure it wasn't corrupted.

## Performance Considerations

For large files (>100 MB):
- **BLAKE2/BLAKE2b**: Best performance
- **SHA512**: Good performance
- **SHA256**: Standard performance
- **MD5**: Acceptable but outdated

EncryptoCLI uses chunked reading (1024 bytes at a time) to handle large files efficiently without loading them entirely into memory.

## Security Notes

⚠️ **Important**: Hashing is one-way. You **cannot** recover the original data from a hash.

✅ **Best Practices**:
- Use BLAKE2b for new applications
- Use SHA256 if BLAKE2b is not available
- Avoid MD5 for security-critical applications
- Always use unique salts when implementing password hashing (not applicable to EncryptoCLI's general-purpose hashing)
