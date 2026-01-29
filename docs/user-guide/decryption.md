# Decryption

Decrypt data that was previously encrypted with EncryptoCLI.

## Decrypt Text

1. Launch EncryptoCLI: `encryptocli`
2. Select "Decrypt" operation
3. Choose "Text" as data type
4. Paste or enter the encrypted text
5. Select decryption method matching encryption:
   - **AES**: Enter the original password
   - **PGP**: Passphrase will be requested by GPG
6. View decrypted output
7. Copy and use the decrypted text

## Decrypt File

1. Launch EncryptoCLI: `encryptocli`
2. Select "Decrypt" operation
3. Choose "File" as data type
4. Enter the encrypted file path
5. Select decryption method:
   - **AES**: Enter the original password
   - **PGP**: GPG will prompt for passphrase
6. Decrypted file saved as `encryptocli_output.dec`
7. Open or use the decrypted file

## Decrypt from Image (Steganography)

Extract and decrypt hidden data from an image:

1. Launch EncryptoCLI: `encryptocli`
2. Select "Decrypt" operation
3. Choose "Image" as data type
4. Enter the image file path containing hidden data
5. Enter the password used during encryption
6. Select steganography method (LSB or DCT)
7. View extracted and decrypted data

See [Steganography](steganography.md) for more details.

## Troubleshooting

### Wrong Password Error

- **AES**: Password is incorrect
  - Try alternate passwords if you have multiple
  - Ensure CAPS LOCK is off
  - Check for extra spaces

- **PGP**: Passphrase is incorrect
  - Enter the passphrase for your private key
  - Try again if you mistyped

### File Not Found

- Verify the file path is correct
- Check file exists and is readable
- Ensure path has no typos

### Unsupported Format

- File may not be encrypted with EncryptoCLI
- Check file extension and format
- Ensure file wasn't corrupted
- Try with original encryption method

### PGP Key Not Found

- Ensure GPG is installed
- Run `gpg --list-secret-keys` to see your private keys
- Import recipient's public key if needed

## Recovery Options

If you've forgotten a password or passphrase:

- **AES**: No recovery option - password is unrecoverable
- **PGP**: Can create new key pair, but previous encrypted files cannot be recovered

Always keep secure backups of:
- PGP private keys
- Passwords in a password manager
- Passphrases in a secure location
