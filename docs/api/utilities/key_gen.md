# Key Generation

Cryptographic key derivation and generation utilities.

## Functions

### derive_key(password, salt, key_length=32, iterations=100000)

Derive encryption key from password using PBKDF2.

**Parameters:**
- `password` (str): User password
- `salt` (bytes): Random salt (16 bytes typical)
- `key_length` (int): Desired key length in bytes (default: 32)
- `iterations` (int): PBKDF2 iterations (default: 100000)

**Returns:** bytes - Derived key

**Example:**
```python
from encryptocli.util.key_gen import derive_key, generate_salt

salt = generate_salt()
key = derive_key("my_password", salt)
print(f"Derived key: {key.hex()}")
```

### generate_salt(length=16)

Generate cryptographically secure random salt.

**Parameters:**
- `length` (int): Salt length in bytes (default: 16)

**Returns:** bytes - Random salt

**Example:**
```python
from encryptocli.util.key_gen import generate_salt

salt = generate_salt()
print(f"Salt length: {len(salt)} bytes")
```

### generate_iv(length=16)

Generate cryptographically secure random initialization vector.

**Parameters:**
- `length` (int): IV length in bytes (default: 16)

**Returns:** bytes - Random IV

**Example:**
```python
from encryptocli.util.key_gen import generate_iv

iv = generate_iv()
print(f"IV length: {len(iv)} bytes")
```

### generate_random_bytes(length)

Generate cryptographically secure random bytes.

**Parameters:**
- `length` (int): Number of random bytes

**Returns:** bytes - Random bytes

**Example:**
```python
from encryptocli.util.key_gen import generate_random_bytes

random_data = generate_random_bytes(32)
print(f"Generated {len(random_data)} random bytes")
```

## Key Derivation Details

### PBKDF2 Algorithm

- **Hash Function**: SHA-256
- **Iterations**: 100,000 (configurable)
- **Output Length**: 32 bytes (256 bits)

### Security

- Slow intentional computation resists brute force
- Random salt prevents rainbow tables
- 100,000 iterations provides strong security
- Industry standard algorithm

## Usage Examples

### Basic Key Derivation

```python
from encryptocli.util.key_gen import derive_key, generate_salt

# Generate salt
salt = generate_salt()

# Derive key
key = derive_key("my_password", salt)

print(f"Salt: {salt.hex()}")
print(f"Key: {key.hex()}")
```

### Encrypt with Derived Key

```python
from cryptography.fernet import Fernet
from encryptocli.util.key_gen import derive_key, generate_salt
import base64

# Generate salt
salt = generate_salt()

# Derive key for Fernet
key = derive_key("password", salt)
fernet_key = base64.b64encode(key)

# Create cipher
cipher_suite = Fernet(fernet_key)

# Encrypt
plaintext = "secret message"
ciphertext = cipher_suite.encrypt(plaintext.encode())

print(f"Salt: {salt.hex()}")
print(f"Ciphertext: {ciphertext.decode()}")
```

### Multiple Key Generation

```python
from encryptocli.util.key_gen import derive_key, generate_salt

# Generate different keys for different purposes
encryption_salt = generate_salt()
encryption_key = derive_key("password", encryption_salt)

signing_salt = generate_salt()
signing_key = derive_key("password", signing_salt)

print("Encryption key:", encryption_key.hex())
print("Signing key:", signing_key.hex())
```

### Configurable Key Derivation

```python
from encryptocli.util.key_gen import derive_key, generate_salt

salt = generate_salt()

# Standard security (100,000 iterations)
key1 = derive_key("password", salt)

# High security (200,000 iterations)
key2 = derive_key("password", salt, iterations=200000)

# Low security/fast (10,000 iterations)
key3 = derive_key("password", salt, iterations=10000)

print(f"Standard: {key1.hex()}")
print(f"High security: {key2.hex()}")
print(f"Fast: {key3.hex()}")
```

### Random IV Generation

```python
from encryptocli.util.key_gen import generate_iv, generate_salt

# Generate IVs for CBC mode
iv1 = generate_iv()
iv2 = generate_iv()

# Verify they're different
assert iv1 != iv2, "IVs should be random"

print(f"IV1: {iv1.hex()}")
print(f"IV2: {iv2.hex()}")
```

## Security Best Practices

### 1. Use Strong Passwords

```python
# Good: Long, varied character password
password = "Tr0pical!BlueMoon$2024"

# Bad: Simple dictionary words
password = "password123"
```

### 2. Random Salts

```python
from encryptocli.util.key_gen import generate_salt, derive_key

# Always generate random salt
salt = generate_salt()

# Never reuse salt with same password
key = derive_key("password", salt)
```

### 3. Sufficient Iterations

```python
from encryptocli.util.key_gen import derive_key, generate_salt

salt = generate_salt()

# Use default iterations (100,000)
key = derive_key("password", salt)

# Or higher for extra security
key = derive_key("password", salt, iterations=200000)
```

### 4. Independent Keys

```python
from encryptocli.util.key_gen import derive_key, generate_salt

# Use different salts for different keys
salt1 = generate_salt()
salt2 = generate_salt()

key1 = derive_key("password", salt1)
key2 = derive_key("password", salt2)

# Keys will be different
assert key1 != key2
```

## Performance

### Time Complexity

Key derivation involves intentional computation to resist brute force attacks.

### Recommendations

Key derivation security depends on proper configuration:
- Use recommended iteration count
- Always use random salts
- Use sufficient key length for your application

## Cryptographic Security

### Entropy Sources

- Uses `os.urandom()` for randomness
- Cryptographically secure
- Platform-independent
- Thread-safe

### PBKDF2 Details

- **Hash Algorithm**: SHA-256
- **Output Size**: 32 bytes (256 bits)
- **Salt Size**: 16 bytes (128 bits)
- **Iterations**: Configurable

### Key Strength

- 256-bit keys suitable for AES-256
- 128-bit keys suitable for AES-128
- Higher iterations increase security

## See Also

- [File Handling](file_handling.md)
- [Exceptions](exceptions.md)
- [AES Cipher](../encryption/aes_cipher.md)
