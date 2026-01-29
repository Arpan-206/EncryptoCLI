# PGP Key Management

Manage your PGP keys for secure asymmetric encryption.

## Prerequisites

- **GPG installed** on your system
  - macOS: `brew install gnupg`
  - Ubuntu/Debian: `sudo apt-get install gnupg`
  - Windows: Download from [gnupg.org](https://www.gnupg.org/download/)

## Key Concepts

### Public Key

- Can be shared freely with anyone
- Used to encrypt data for you
- Others use it to verify your digital signatures

### Private Key

- Keep absolutely secret and secure
- Used to decrypt data encrypted with your public key
- Never share this key
- Protected by passphrase

### Key Pair

- Public and private keys work together
- Create both when generating a new key
- Used for secure communication

## Generate a New Key Pair

### Using GPG Command Line

```bash
gpg --gen-key
```

Follow the prompts:

1. Select key type (default RSA and RSA is fine)
2. Select key size (4096 bits recommended for security)
3. Set expiration date (0 = no expiration recommended)
4. Enter real name
5. Enter email address
6. Add comment (optional)
7. Set passphrase (use strong passphrase)

### Verify Key Creation

```bash
gpg --list-secret-keys
```

Shows your private keys with key IDs and details.

## List Keys

### View All Keys

```bash
gpg --list-keys
```

Shows all public keys (yours and imported ones).

### View Secret Keys Only

```bash
gpg --list-secret-keys
```

Shows only your private keys.

### View Key Details

```bash
gpg --list-keys --with-fingerprint
```

Shows keys with additional fingerprint information.

## Export Keys

### Export Public Key

```bash
gpg --export --armor YOUR_EMAIL > public_key.asc
```

Share this file with anyone who needs to encrypt data for you.

### Export Private Key

```bash
gpg --export-secret-keys --armor YOUR_EMAIL > private_key.asc
```

Keep this file secure. Never share it.

## Import Keys

### Import Public Key

```bash
gpg --import public_key.asc
```

Import someone else's public key to encrypt data for them.

### Import Private Key

```bash
gpg --import private_key.asc
```

Restore your private key from backup.

## Delete Keys

### Delete Public Key

```bash
gpg --delete-key EMAIL_OR_ID
```

### Delete Private Key

```bash
gpg --delete-secret-key EMAIL_OR_ID
```

Warning: This cannot be undone without restoring from backup.

## Key Backup and Recovery

### Backup Your Keys

```bash
# Backup private key
gpg --export-secret-keys --armor > backup_private_key.asc

# Backup all public keys
gpg --export --armor > backup_public_keys.asc
```

Store backups securely:
- Encrypted external drive
- Secure cloud storage (encrypted)
- Physical storage in safe
- Multiple redundant backups

### Restore From Backup

```bash
gpg --import backup_private_key.asc
gpg --import backup_public_keys.asc
```

## Using with EncryptoCLI

### Encrypt for Someone

1. Import their public key: `gpg --import their_public_key.asc`
2. In EncryptoCLI, select "Encrypt" with PGP method
3. Enter their email address
4. Data is encrypted with their public key

### Decrypt Your Messages

1. EncryptoCLI detects encrypted data
2. You'll be prompted for your passphrase
3. GPG uses your private key to decrypt
4. Decrypted data is displayed

## Security Best Practices

- Use strong passphrases (20+ characters)
- Store backups in multiple secure locations
- Never share your private key
- Verify key fingerprints before importing keys from others
- Regularly review and update your key expiration dates
- Use key signing to build trust in your key network

## Common Issues

### "GPG not found"

- Install GPG using package manager
- Ensure GPG is in system PATH

### "No secret key"

- Check you generated a key pair: `gpg --list-secret-keys`
- Ensure you know the email associated with your key

### "Wrong passphrase"

- Passphrase is case-sensitive
- Ensure CAPS LOCK is off
- Try again carefully

### Key Not Found by Email

- List all keys: `gpg --list-keys`
- Verify exact email address format
- Check if key might use different email
