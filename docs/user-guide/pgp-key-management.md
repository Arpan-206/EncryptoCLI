# PGP Key Management Commands

## Overview

PGP key management commands have been added to both the CLI and TUI interfaces, allowing users to generate, import, export, and list PGP keys directly from EncryptoCLI.

## CLI Commands

### Generate Key Pair

Generate a new PGP key pair (RSA 2048-bit).

```bash
encryptocli pgp-gen-key
# or with options:
encryptocli pgp-gen-key --name "John Doe" --email "john@example.com" --passphrase "secure_pass"
```

**Options:**
- `--name, -n`: Full name for the key (required)
- `--email, -e`: Email address for the key (required)
- `--passphrase, -p`: Passphrase to protect the key (required, hidden input)

**Output:**
```
PGP Key Generated Successfully!
Fingerprint: 1234567890ABCDEF...
Email: john@example.com
```

### Export Public Key

Export a public key to a file for sharing.

```bash
encryptocli pgp-export-key
# or with options:
encryptocli pgp-export-key --email "john@example.com" --output "john_public.asc"
```

**Options:**
- `--email, -e`: Email address of the key to export (required)
- `--output, -o`: Output file path (default: public_key.asc)

**Output:**
```
Public key exported to john_public.asc
```

### Import Public Key

Import a public key from a file.

```bash
encryptocli pgp-import-key
# or with option:
encryptocli pgp-import-key --file "recipient_public.asc"
```

**Options:**
- `--file, -f`: Path to the public key file (required)

**Output:**
```
Public key imported successfully. Fingerprint: ABC123...
```

### List Keys

List all available PGP keys in the keyring.

```bash
encryptocli pgp-list-keys
```

**Output:**
```
=== PGP Keys ===

1. John Doe <john@example.com>
   Type: pub
   Key ID: 1234567890ABCDEF
   Fingerprint: 1234567890ABCDEF1234567890ABCDEF12345678

2. Alice Smith <alice@example.com>
   Type: pub
   Key ID: FEDCBA0987654321
   Fingerprint: FEDCBA0987654321FEDCBA0987654321FEDCBA09
```

## TUI Interface

The TUI interface now includes a "PGP Keys" option in the main menu:

```
What do you want to do?
> Hash
  Encrypt
  Decrypt
  PGP Keys
  Exit
```

### Generate Key Pair (TUI)

Select "PGP Keys" → "Generate Key Pair" to:
1. Enter your full name
2. Enter your email address
3. Enter a passphrase to protect your key

The system will generate and display:
- Your full name
- Email address
- Key fingerprint

### List Keys (TUI)

Select "PGP Keys" → "List Keys" to view all keys in your keyring with:
- Email address (UID)
- Key ID
- Fingerprint

### Import Public Key (TUI)

Select "PGP Keys" → "Import Public Key" to:
1. Provide the path to the public key file
2. Confirm successful import with fingerprint

### Export Public Key (TUI)

Select "PGP Keys" → "Export Public Key" to:
1. Enter the email of the key to export
2. Specify output file path (default: public_key.asc)
3. Confirm successful export

## Usage Examples

### Example 1: Generate a Key Pair and Share It

```bash
# Generate your key pair
encryptocli pgp-gen-key

# Export your public key for sharing
encryptocli pgp-export-key --email "you@example.com" --output "my_public_key.asc"

# Send the file to others or upload to a key server
```

### Example 2: Import a Recipient's Key and Encrypt

```bash
# Import recipient's public key
encryptocli pgp-import-key --file "recipient_public.asc"

# List keys to verify it was imported
encryptocli pgp-list-keys

# Now you can encrypt for them
encryptocli encrypt --text "Secret message" --password "recipient@example.com" --method pgp
```

### Example 3: Key Management Workflow (TUI)

```
1. Run: python -m encryptocli
2. Select: PGP Keys
3. Select: Generate Key Pair
4. Enter: Name, Email, Passphrase
5. Success! Key generated with fingerprint
6. Later, to share: PGP Keys → Export Public Key
7. Or receive: PGP Keys → Import Public Key
```

## Key Management Best Practices

### 1. **Backup Your Keys**
After generating a key, export and safely backup your private key:
```bash
# The private key is only available locally
# Consider exporting and encrypting it with a strong passphrase
```

### 2. **Share Your Public Key**
```bash
# Export your public key for others
encryptocli pgp-export-key --email "you@example.com"

# Share via email, upload to keyserver, or post online
```

### 3. **Verify Key Fingerprints**
When importing a key, always verify the fingerprint through a trusted channel (call, video, in-person) before using it:
```bash
# See the fingerprint when importing
encryptocli pgp-import-key --file "key.asc"

# List keys to see fingerprints anytime
encryptocli pgp-list-keys
```

### 4. **Protect Your Passphrase**
- Use a strong, unique passphrase
- Never share your passphrase
- Store it in a secure password manager
- Use the hidden input prompt (auto-masked)

## File Management

### Key Files
- **Public Key Format**: `.asc` (ASCII-armored PGP format)
- **Import/Export**: Uses standard OpenPGP format
- **Compatibility**: Compatible with other PGP/GPG tools

### Example File Structure

```
my_keys/
├── john_public.asc       # Public key for sharing
├── alice_public.asc      # Imported public key
└── backup_key.asc        # Backup of your public key
```

## Integration with Encryption

Once keys are set up, use them immediately:

```bash
# Using CLI
encryptocli encrypt --text "Message" --password "recipient@example.com" --method pgp

# Using TUI
Select: Encrypt → Text/File → PGP → Enter recipient email
```

## Common Workflows

### Secure Communication Setup

```bash
# User A: Generate and share
encryptocli pgp-gen-key  # Interactive setup
encryptocli pgp-export-key --email "a@example.com" --output "a_public.asc"
# Send a_public.asc to User B

# User B: Import and send reply
encryptocli pgp-import-key --file "a_public.asc"
encryptocli pgp-gen-key  # Generate own key
encryptocli pgp-export-key --email "b@example.com" --output "b_public.asc"
# Send b_public.asc to User A

# User A: Import User B's key
encryptocli pgp-import-key --file "b_public.asc"

# Both can now encrypt/decrypt messages for each other
```

### Key List Reference

```bash
# Anytime you need to see available keys and their emails
encryptocli pgp-list-keys

# Use the email from the list when encrypting
encryptocli encrypt --text "Message" --password "b@example.com" --method pgp
```

## Troubleshooting

### "Key not found" error
```bash
# Verify the key exists
encryptocli pgp-list-keys

# Generate a new key if needed
encryptocli pgp-gen-key
```

### "Import failed" error
- Ensure the file is a valid PGP public key (.asc format)
- Check that the file path is correct
- Try opening the file to verify its format

### Passphrase Issues
```bash
# If you forget your passphrase, you'll need to generate a new key
# The old key remains but is inaccessible
encryptocli pgp-gen-key  # Create new key with new passphrase
```

### Key Listing Empty
```bash
# If no keys appear, you need to generate or import one
encryptocli pgp-gen-key  # Generate your own
# OR
encryptocli pgp-import-key  # Import someone else's
```

## Advanced: Manual Key Management

If you need to work with keys outside EncryptoCLI:

```bash
# Export using GPG directly
gpg --export your@email.com > your_public.asc
gpg --export-secret-keys your@email.com > your_private.asc  # Keep safe!

# Import using GPG directly
gpg --import public_key.asc

# List keys using GPG
gpg --list-keys
```

These keys will be recognized by EncryptoCLI.

## See Also

- [PGP User Guide](./docs/user-guide/pgp.md)
- [PGP API Reference](./docs/api/encryption/pgp.md)
- [GnuPG Documentation](https://www.gnupg.org/documentation/)
