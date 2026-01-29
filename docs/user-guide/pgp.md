# PGP Encryption Support

EncryptoCLI now includes support for **Pretty Good Privacy (PGP)** encryption in addition to the existing AES (Fernet) encryption method. PGP provides asymmetric encryption, which is ideal for secure communication between multiple parties.

## What is PGP?

PGP (Pretty Good Privacy) is a cryptographic software that provides:
- **Asymmetric Encryption**: Uses public and private key pairs
- **Digital Signatures**: Verify authenticity and integrity of messages
- **Key Management**: Create and manage cryptographic keys
- **Wide Compatibility**: Industry standard for secure communication

## Key Storage

PGP keys are stored in your system's **persistent GPG keyring** (`~/.gnupg/`):
- ✅ Keys persist across program restarts
- ✅ Compatible with system GPG tools
- ✅ Private keys encrypted with your passphrase
- ✅ Can be backed up and restored
- 🔒 Protected with file permissions (700)

For key management commands, see the [PGP Key Management Guide](pgp-key-management.md).

## Key Differences: PGP vs AES

| Feature | PGP | AES |
|---------|-----|-----|
| Encryption Type | Asymmetric (Public/Private Keys) | Symmetric (Password-based) |
| Key Management | Complex (Key pairs) | Simple (Password only) |
| Key Persistence | Yes (~/.gnupg/) | N/A (password-based) |
| Multiple Recipients | Yes | No |
| Use Case | Secure communication, Digital signatures | Quick file encryption |
| Learning Curve | Steep | Shallow |

## Installation

PGP support is included with EncryptoCLI. The required dependency is `python-gnupg`. If upgrading from an older version:

```bash
pip install -r requirements.txt
# or
pip install python-gnupg
```

## Usage

### CLI Usage

#### Encrypt Text with PGP
```bash
encryptocli encrypt --text "Hello, World!" --password recipient@example.com --method pgp
```

#### Decrypt Text with PGP
```bash
encryptocli decrypt --text "<encrypted_data>" --password "your_passphrase" --method pgp
```

#### Encrypt File with PGP
```bash
encryptocli encrypt --file document.pdf --password recipient@example.com --method pgp
```

#### Decrypt File with PGP
```bash
encryptocli decrypt --file document.pdf.pgp --password "your_passphrase" --method pgp --output ./decrypted/
```

### TUI (Text User Interface) Usage

The TUI interface now provides a menu to select the encryption method:

```
What do you want to encrypt?
> Text
  File

Which encryption method do you want to use?
> AES (Fernet)
  PGP

[Follow prompts for recipient email or password]
```

## How PGP Works in EncryptoCLI

### Encryption Flow

1. **Generate/Import Key Pair**
   - Create a new key pair with name, email, and passphrase
   - Or import an existing public key

2. **Encrypt Data**
   - Use recipient's email to find their public key
   - Encrypt data with their public key
   - Only they can decrypt with their private key

3. **Decrypt Data**
   - Use your private key (protected by passphrase)
   - Decrypt data encrypted with your public key

### Example Workflow

**User A (Sender):**
```python
from encryptocli.encryption.pgp import PGPCipher

pgp = PGPCipher()

# Encrypt message for User B
encrypted = pgp.encrypt_text(
    "Secret message",
    "userb@example.com"
)
```

**User B (Recipient):**
```python
# Decrypt message using their passphrase
decrypted = pgp.decrypt_text(
    encrypted,
    passphrase="my_passphrase"
)
```

## Python API

### PGPCipher Class

```python
from encryptocli.encryption.pgp import PGPCipher

pgp = PGPCipher()
```

#### Generate Key Pair
```python
fingerprint = pgp.generate_key_pair(
    name="John Doe",
    email="john@example.com",
    passphrase="secure_passphrase"
)
print(f"Key generated: {fingerprint}")
```

#### Encrypt Text
```python
encrypted = pgp.encrypt_text(
    secret="Hello, World!",
    recipient_email="recipient@example.com",
    passphrase=None  # Optional, for signing
)
```

#### Decrypt Text
```python
decrypted = pgp.decrypt_text(
    encrypted_secret=encrypted,
    passphrase="your_passphrase"
)
print(decrypted)
```

#### Encrypt File
```python
result = pgp.encrypt_file(
    file_path="document.pdf",
    recipient_email="recipient@example.com"
)
print(result)  # "File encrypted successfully"
```

#### Decrypt File
```python
result = pgp.decrypt_file(
    file_path="document.pdf.pgp",
    passphrase="your_passphrase",
    output_dir="./"
)
print(result)
```

#### Export Public Key
```python
result = pgp.export_public_key(
    email="john@example.com",
    output_path="john_public.asc"
)
```

#### Import Public Key
```python
result = pgp.import_public_key(
    key_path="recipient_public.asc"
)
```

#### List Keys
```python
keys = pgp.list_keys()
for key in keys:
    print(f"Email: {key['uids']}, Fingerprint: {key['keyid']}")
```

## Advanced: Using Services

```python
from encryptocli.services import EncryptionService, DecryptionService

# Encryption
encryption_service = EncryptionService()
encrypted = encryption_service.encrypt_text(
    secret="Sensitive data",
    password="recipient@example.com",
    method="pgp"
)

# Decryption
decryption_service = DecryptionService()
decrypted = decryption_service.decrypt_text(
    data=encrypted,
    password="passphrase",
    method="pgp"
)
```

## Key Management Best Practices

### 1. **Passphrase Security**
- Use strong, unique passphrases for your private keys
- Never share your passphrase or private key
- Store passphrases securely (password manager)

### 2. **Key Backup**
```bash
# Export your private key (keep it safe!)
gpg --export-secret-keys your@email.com > private_key.asc
```

### 3. **Key Distribution**
```bash
# Share your public key with others
gpg --export your@email.com > public_key.asc
# Send via email or upload to key server
```

### 4. **Key Verification**
Always verify key fingerprints through a trusted channel before using them:
```bash
gpg --fingerprint recipient@example.com
```

## Steganography with PGP

Combine PGP encryption with steganography to hide encrypted data in images:

```bash
# Encrypt text with PGP and hide in image
encryptocli encrypt \
  --text "Secret message" \
  --image image.png \
  --password recipient@example.com \
  --method pgp

# Decrypt from image with PGP
encryptocli decrypt \
  --image encrypted_image.png \
  --password "passphrase" \
  --method pgp
```

## Troubleshooting

### "python-gnupg is required"
Install the missing dependency:
```bash
pip install python-gnupg
```

### "Recipient key not found"
Import the recipient's public key:
```python
pgp.import_public_key("recipient_public.asc")
```

### "Decryption failed"
- Verify you're using the correct passphrase
- Ensure the encrypted data is valid
- Check that your private key is available

### GPG Not Installed
Some systems require GPG to be installed separately:

**macOS:**
```bash
brew install gnupg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install gnupg
```

**Windows:**
Download from [gnupg.org](https://www.gnupg.org/download/)

## Security Considerations

1. **Key Length**: Uses RSA 2048-bit keys (balance of security and speed)
2. **Trust Model**: Uses `always_trust=True` for convenience (consider implementing GPG trust model for production)
3. **Passphrase**: Protects private keys; never hardcode passphrases
4. **Temporary Files**: Keys stored in temporary GPG home directory (auto-cleaned)

## Comparing with Other Tools

### vs OpenPGP
- More user-friendly CLI interface
- Integrated with steganography features
- Simplified key management

### vs GnuPG (Command-line)
- Easier to use via Python API
- Integrated encryption/steganography pipeline
- Multi-method support (AES + PGP)

### vs Hardware Security Keys
- Software-based (no additional hardware needed)
- Lower security than hardware keys
- Better for general-purpose use

## See Also

- [GnuPG Documentation](https://www.gnupg.org/documentation/)
- [Python-gnupg](https://python-gnupg.readthedocs.io/)
- [PGP Basics](https://en.wikipedia.org/wiki/Pretty_Good_Privacy)
