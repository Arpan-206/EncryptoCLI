# Encryption Guide

Encryption is the process of converting readable data (plaintext) into unreadable data (ciphertext) using a password. Only someone with the correct password can decrypt the data back to its original form.

## Encryption Methods

EncryptoCLI supports two encryption methods:

### 1. Text Encryption
Encrypt text data and output it as encrypted text or hide it in an image.

### 2. File Encryption
Encrypt entire files and save them with a `.encrypto` extension.

## How Encryption Works

EncryptoCLI uses **Fernet encryption** from the cryptography library, which provides:

- **Symmetric encryption**: Same password encrypts and decrypts data
- **Key derivation**: Your password is converted to a cryptographic key using scrypt
- **Authentication**: Ensures data hasn't been tampered with
- **Randomization**: Each encryption produces different output (even with same password)

## Encrypting Text

### Step 1: Select Encryption

From the main menu, select **Encrypt**:

```
? What do you want to do?
❯ Encrypt
```

### Step 2: Choose Data Type

Select **Text**:

```
? What do you want to encrypt?
❯ Text
  File
```

### Step 3: Choose Output Format

Select how to output the encrypted data:

```
? What do you want to encrypt to?
❯ Image
  Text
```

#### Option A: Output as Text

1. You'll be asked for the text to encrypt:
   ```
   ? Enter the text to encrypt: My secret message
   ```

2. Enter a strong password:
   ```
   ? Enter the password: ••••••••
   ```

3. View the encrypted output:
   ```
   The encrypted text is: gAAAAABl...
   ```

#### Option B: Hide in Image (Steganography)

1. Provide the path to a PNG image:
   ```
   ? Enter the path to the image. ( PNG file recommended ): /path/to/image.png
   ```

2. Enter the text to encrypt:
   ```
   ? Enter the text to encrypt: My secret message
   ```

3. Enter a password:
   ```
   ? Enter the password: ••••••••
   ```

4. The encrypted file will be saved as `encrypto.png` in the current directory.

## Encrypting Files

### Step 1-2: Select File Encryption

1. From the main menu, select **Encrypt**
2. Choose **File**:

```
? What do you want to encrypt?
❯ File
```

### Step 3: Provide File Path

Enter the path to the file you want to encrypt:

```
? Enter the path to the file: /path/to/document.pdf
```

### Step 4: Enter Password

Create a strong password:

```
? Enter the password: ••••••••
```

### Step 5: Done

The encrypted file will be created with a `.encrypto` extension:

```
File encrypted successfully.
document.pdf.encrypto
```

## Password Guidelines

⚠️ **Important**: Your password determines your security level!

### Strong Password Characteristics

- **Length**: Minimum 12 characters (16+ recommended)
- **Complexity**: Mix of uppercase, lowercase, numbers, and symbols
- **Uniqueness**: Don't reuse passwords across applications
- **Memorability**: Create a passphrase if needed

### Examples

❌ **Weak Passwords**:
- `password`
- `12345678`
- `qwerty`
- `abc123`

✅ **Strong Passwords**:
- `BlueMoon$Galaxy#2024!`
- `CryptoKeeper@Secure7X`
- `MyDogHas3Legs&Wings`

### Password Recovery

⚠️ **Critical**: If you lose your password, **your data cannot be recovered**. There is no password reset or recovery mechanism.

## Security Best Practices

✅ **Do**:
- Use unique, strong passwords
- Store passwords securely (password manager recommended)
- Back up encrypted files
- Test decryption on a copy first
- Use PNG format for steganography

❌ **Don't**:
- Share passwords over insecure channels
- Use the same password for multiple files
- Store passwords in plain text
- Forget your password
- Assume encrypted data is secure forever (use regular algorithms)

## File Size Limits

- **Maximum file size**: 1 GB
- **Recommended size**: < 500 MB
- **Note**: Larger files may take longer to encrypt

## Examples

### Example 1: Encrypt a Document

```bash
# Encrypt a PDF
? What do you want to encrypt? File
? Enter the path to the file: ~/Documents/report.pdf
? Enter the password: MySecurePassword123!
File encrypted successfully.
→ ~/Documents/report.pdf.encrypto
```

### Example 2: Hide a Message in an Image

```bash
# Hide a message
? What do you want to encrypt? Text
? What do you want to encrypt to? Image
? Enter the path to the image: ~/Pictures/vacation.png
? Enter the text to encrypt: "Meet me at the secret location"
? Enter the password: MySecurePassword123!
→ encrypto.png
```

## Troubleshooting

### "File not found" error
- Double-check the file path
- Use absolute paths instead of relative paths
- Ensure file exists and you have read permission

### "File is already encrypted" error
- Don't encrypt already encrypted files
- If needed, decrypt first, then re-encrypt with new password

### Encryption takes too long
- This is normal for large files (1 GB might take a few minutes)
- Ensure your system has sufficient RAM
- Avoid encrypting over network drives
