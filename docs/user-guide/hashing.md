# Hashing

Generate cryptographic hashes for text or files using various algorithms.

## Overview

Hashing creates a unique, fixed-size digest from any input data. Identical inputs always produce identical hashes, but changing even one character produces a completely different hash.

## Supported Algorithms

EncryptoCLI supports 13 hash algorithms:

| Algorithm | Use Case | Output Size |
|-----------|----------|------------|
| MD5 | Legacy, not cryptographically secure | 128 bits |
| SHA1 | Legacy, deprecated for cryptography | 160 bits |
| SHA224 | General purpose | 224 bits |
| SHA256 | Modern, widely used | 256 bits |
| SHA384 | Higher security | 384 bits |
| SHA512 | Maximum SHA security | 512 bits |
| SHA3-224 | Modern alternative | 224 bits |
| SHA3-256 | Modern alternative | 256 bits |
| SHA3-384 | Modern alternative | 384 bits |
| SHA3-512 | Modern alternative | 512 bits |
| BLAKE2s | Fast, secure | 256 bits |
| BLAKE2b | Fast, secure | 512 bits |
| BLAKE3 | Latest, highly efficient | 256 bits |

## Hash Text

1. Launch EncryptoCLI: `encryptocli`
2. Select "Hash" operation
3. Choose "Text" as data type
4. Enter the text to hash
5. Select your desired algorithm
6. View the generated hash

## Hash File

1. Launch EncryptoCLI: `encryptocli`
2. Select "Hash" operation
3. Choose "File" as data type
4. Enter the file path
5. Select your desired algorithm
6. View the generated hash

## Recommendations

- **General Purpose**: Use SHA256 or SHA3-256
- **High Security**: Use SHA512 or BLAKE3
- **Legacy Systems**: Use SHA1 or MD5 (only if required)
- **Performance**: Use BLAKE2 or BLAKE3 for fastest hashing

## Use Cases

- **File Integrity**: Hash a file before distribution to verify it hasn't been modified
- **Password Storage**: Hash passwords securely (though dedicated tools are recommended)
- **Duplicate Detection**: Compare hashes to find identical files
- **Data Verification**: Confirm data authenticity
