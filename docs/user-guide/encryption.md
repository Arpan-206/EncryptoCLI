# Encryption

Encrypt your sensitive data using AES or PGP encryption methods.

## Encryption Methods

### AES (Advanced Encryption Standard)

Symmetric encryption using Fernet (authenticated encryption).

- **Advantages**:
  - Fast and efficient
  - Requires only a password
  - Works with any file type
  - No key setup needed

- **Disadvantages**:
  - Password must be shared securely
  - Same password used to encrypt and decrypt

- **Best For**: Quick encryption of personal files, documents, images

### PGP (Pretty Good Privacy)

Asymmetric encryption using public key cryptography.

- **Advantages**:
  - Public key can be shared openly
  - Only recipient with private key can decrypt
  - Strong security guarantees
  - Industry standard

- **Disadvantages**:
  - Requires GPG installation
  - Key setup and management required
  - More complex workflow

- **Best For**: Secure communication, file sharing with specific recipients

## Encrypt Text

1. Launch EncryptoCLI: `encryptocli`
2. Select "Encrypt" operation
3. Choose "Text" as data type
4. Enter the text to encrypt
5. Select encryption method:
   - **AES**: Enter a strong password
   - **PGP**: Enter recipient's email address
6. Receive encrypted output
7. Copy and save the encrypted text

## Encrypt File

1. Launch EncryptoCLI: `encryptocli`
2. Select "Encrypt" operation
3. Choose "File" as data type
4. Enter the file path to encrypt
5. Select encryption method:
   - **AES**: Enter a strong password
   - **PGP**: Enter recipient's email address
6. Encrypted file saved as `encryptocli_output.enc`
7. Store securely

## Encrypt to Image (Steganography)

Hide encrypted data inside an image:

1. Launch EncryptoCLI: `encryptocli`
2. Select "Encrypt" operation
3. Choose "Image" as output type
4. Provide the image file path
5. Enter text to encrypt and hide
6. Set a password
7. Encrypted data is hidden in the image
8. Visual appearance of image remains unchanged

See [Steganography](steganography.md) for more details.

## Security Tips

- **AES**: Use strong, unique passwords
  - Minimum 12 characters
  - Mix uppercase, lowercase, numbers, symbols
  - Avoid dictionary words

- **PGP**: Protect your private key
  - Store in secure location
  - Use strong passphrase
  - Backup securely

- **General**: 
  - Only encrypt data you need to protect
  - Keep encrypted files organized
  - Remember your passwords/passphrases
  - Share encrypted files through secure channels

## Supported File Types

All file types are supported:
- Documents (.pdf, .docx, .txt, etc.)
- Images (.jpg, .png, .gif, etc.)
- Archives (.zip, .tar, .rar, etc.)
- Executables (.exe, .sh, etc.)
- Any binary or text file

## Output Format

Encrypted data is stored in a binary-safe format that preserves all data integrity.
