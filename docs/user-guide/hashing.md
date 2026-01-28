# Hashing Guide

Hashing is a one-way function that converts data into a fixed-size string of characters. It's commonly used for password storage, data integrity verification, and digital signatures.

## Supported Algorithms

EncryptoCLI supports **14 industry-standard hashing algorithms**:

### Legacy Algorithms

#### MD5
- **Speed**: Very Fast
- **Output Size**: 128 bits (32 hex characters)
- **Use Case**: Legacy applications (NOT recommended for security-critical applications)
- **Note**: Cryptographically broken, use only when required for compatibility

#### SHA1
- **Speed**: Very Fast
- **Output Size**: 160 bits (40 hex characters)
- **Use Case**: Legacy applications (NOT recommended for new projects)
- **Note**: Deprecated for security purposes, but still used in Git

### SHA-2 Family (Recommended)

#### SHA224, SHA256, SHA384, SHA512
- **Speed**: Fast
- **Output Sizes**: 224, 256, 384, or 512 bits
- **Use Case**: Recommended for most applications
- **Note**: Widely trusted and used across the industry (TLS, Bitcoin, etc.)

### SHA-3 Family (Modern)

#### SHA3_224, SHA3_256, SHA3_384, SHA3_512
- **Speed**: Fast
- **Output Sizes**: 224, 256, 384, or 512 bits
- **Use Case**: Modern alternative to SHA-2
- **Note**: Based on Keccak algorithm, provides different security properties

### BLAKE Family (High Performance)

#### BLAKE2S, BLAKE2B
- **Speed**: Fastest
- **Output Sizes**: 256 bits (BLAKE2S), 512 bits (BLAKE2B)
- **Use Case**: Performance-critical applications
- **Note**: Faster than MD5, SHA-2, and SHA-3 while providing strong security

#### BLAKE3
- **Speed**: Extremely Fast (parallelizable)
- **Output Size**: 256 bits (default, extendable)
- **Use Case**: Modern high-performance applications
- **Note**: Newest BLAKE variant, optimized for modern CPUs with SIMD support

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

Select your preferred algorithm (14 available):

```
? Which algorithm do you want to use?
❯ BLAKE2B
  BLAKE2S
  BLAKE3
  MD5
  SHA1
  SHA224
  SHA256
  SHA384
  SHA512
  SHA3_224
  SHA3_256
  SHA3_384
  SHA3_512
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
