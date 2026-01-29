# PGP Cipher

Asymmetric encryption using GNU Privacy Guard (GPG).

## Class: PGPCipher

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()
```

## Requirements

- **GPG installed**: `brew install gnupg` (macOS), `apt-get install gnupg` (Linux)
- **Key pair generated**: `gpg --gen-key`
- **Public keys imported** for encryption targets

## Methods

### encrypt(plaintext, recipient_email)

Encrypt plaintext for specified recipient.

**Parameters:**
- `plaintext` (str): Text to encrypt
- `recipient_email` (str): Recipient's email address (must be in keyring)

**Returns:** str - Armored PGP-encrypted text

**Raises:**
- `EncryptionError` - If encryption fails or key not found

**Example:**
```python
cipher = PGPCipher()
encrypted = cipher.encrypt("secret", "alice@example.com")
print(encrypted)
```

### decrypt(ciphertext, passphrase=None)

Decrypt ciphertext using private key.

**Parameters:**
- `ciphertext` (str): PGP-encrypted text (armored format)
- `passphrase` (str): Private key passphrase (optional if cached)

**Returns:** str - Decrypted plaintext

**Raises:**
- `DecryptionError` - If password wrong or decryption fails

**Example:**
```python
cipher = PGPCipher()
decrypted = cipher.decrypt(encrypted, passphrase="my_passphrase")
print(decrypted)
```

### list_keys()

List all public keys in keyring.

**Returns:** list - List of key information dictionaries

**Example:**
```python
cipher = PGPCipher()
for key in cipher.list_keys():
    print(f"{key['keyid']}: {key['name']} <{key['email']}>")
```

### list_secret_keys()

List all private keys in keyring.

**Returns:** list - List of private key information dictionaries

**Example:**
```python
cipher = PGPCipher()
for key in cipher.list_secret_keys():
    print(f"Key ID: {key['keyid']}")
    print(f"User: {key['name']}")
    print(f"Email: {key['email']}")
```

### generate_key(name, email, passphrase, key_length=4096)

Generate a new PGP key pair.

**Parameters:**
- `name` (str): Real name for key
- `email` (str): Email address for key
- `passphrase` (str): Passphrase to protect private key
- `key_length` (int): RSA key size in bits (default: 4096)

**Returns:** dict - Generated key information

**Example:**
```python
cipher = PGPCipher()
key = cipher.generate_key(
    "Alice Smith",
    "alice@example.com",
    "secure_passphrase",
    key_length=4096
)
print(f"Generated key: {key['keyid']}")
```

## Key Management

### Import Public Key

```python
import subprocess

# Import from file
subprocess.run(["gpg", "--import", "alice_public_key.asc"])

# Or use Python gnupg library
from python_gnupg import GPG
gpg = GPG()
with open("alice_public_key.asc") as f:
    gpg.import_keys(f.read())
```

### Export Public Key

```python
import subprocess

# Export key for sharing
subprocess.run([
    "gpg",
    "--export",
    "--armor",
    "alice@example.com",
    ">",
    "alice_public_key.asc"
])
```

### Export Private Key (Backup)

```python
import subprocess

# Backup private key
subprocess.run([
    "gpg",
    "--export-secret-keys",
    "--armor",
    "alice@example.com",
    ">",
    "alice_private_key.asc"
])
```

## Usage Examples

### Basic Encryption and Decryption

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()

# Encrypt for Alice
encrypted = cipher.encrypt("confidential data", "alice@example.com")
print(f"Encrypted message:\n{encrypted}")

# Alice decrypts with her passphrase
decrypted = cipher.decrypt(encrypted, passphrase="alice_passphrase")
print(f"Decrypted: {decrypted}")
```

### Workflow with Multiple Users

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()

# Alice generates her key
alice_key = cipher.generate_key(
    "Alice Smith",
    "alice@example.com",
    "alice_passphrase"
)

# Bob generates his key
bob_key = cipher.generate_key(
    "Bob Johnson",
    "bob@example.com",
    "bob_passphrase"
)

# Alice encrypts for Bob
message = "Meet me at noon"
encrypted_for_bob = cipher.encrypt(message, "bob@example.com")

# Bob receives and decrypts
decrypted = cipher.decrypt(encrypted_for_bob, "bob_passphrase")
assert decrypted == message
```

### List Available Keys

```python
from encryptocli.encryption.pgp import PGPCipher

cipher = PGPCipher()

print("Public Keys:")
for key in cipher.list_keys():
    print(f"  {key['keyid']}: {key['name']} <{key['email']}>")

print("\nPrivate Keys:")
for key in cipher.list_secret_keys():
    print(f"  {key['keyid']}: {key['name']} <{key['email']}>")
```

## Error Handling

```python
from encryptocli.encryption.pgp import PGPCipher
from encryptocli.util.exceptions import (
    EncryptionError,
    DecryptionError
)

cipher = PGPCipher()

# Encryption error (key not found)
try:
    encrypted = cipher.encrypt("data", "unknown@example.com")
except EncryptionError as e:
    print(f"Encryption failed: {e}")

# Decryption error (wrong passphrase)
try:
    decrypted = cipher.decrypt(encrypted, "wrong_passphrase")
except DecryptionError as e:
    print(f"Decryption failed: {e}")
```

## Security Best Practices

- Use strong passphrases (20+ characters)
- Store private keys securely
- Backup private keys in secure location
- Never share private keys
- Verify key fingerprints before use
- Keep GPG software updated
- Rotate keys periodically

## Performance

PGP operations involve cryptographic processing that may take time depending on key size and operation complexity.

## Compatibility

- Works with any GPG-compatible software
- Can decrypt emails encrypted with standard PGP tools
- Can encrypt for recipients using any PGP implementation
- Output is industry-standard armored format

## Limitations

- Requires GPG installation
- Key management overhead
- Slower than symmetric encryption
- Recipient must have public key in keyring

## Related Classes

- [AES Cipher](aes_cipher.md)
- [Services - EncryptionService](../services.md)
- [Utilities - Exceptions](../utilities/exceptions.md)
