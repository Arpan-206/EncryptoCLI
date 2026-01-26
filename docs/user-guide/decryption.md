# Decryption Guide

Decryption is the process of converting encrypted data (ciphertext) back to its original readable form using the correct password.

## What Can Be Decrypted

EncryptoCLI can decrypt:

1. **Encrypted text** - Text that was encrypted and output as ciphertext
2. **Encrypted files** - Files with `.encrypto` extension
3. **Steganographic images** - Images containing hidden encrypted data

## How to Decrypt Data

### Decrypting Text

#### Step 1: Select Decryption

From the main menu, select **Decrypt**:

```
? What do you want to do?
❯ Decrypt
```

#### Step 2: Choose Decryption Type

Select **Text**:

```
? What do you want to decrypt?
❯ Text
  File
  Image
```

#### Step 3: Enter Encrypted Text

Paste or enter the encrypted text:

```
? Enter the text to decrypt: gAAAAABl7Hdk...
```

#### Step 4: Enter Password

Enter the password used during encryption:

```
? Enter password: ••••••••
```

#### Step 5: View Result

The decrypted message will be displayed:

```
The decrypted text is: My original message
```

### Decrypting Files

#### Step 1: Select Decryption

From the main menu, select **Decrypt**.

#### Step 2: Choose File Decryption

Select **File**:

```
? What do you want to decrypt?
  Text
❯ File
  Image
```

#### Step 3: Provide Encrypted File Path

Enter the path to the `.encrypto` file:

```
? Enter the path to the file: /path/to/document.pdf.encrypto
```

#### Step 4: Enter Password

Enter the password used during encryption:

```
? Enter password: ••••••••
```

#### Step 5: Done

The decrypted file will be created with the original filename:

```
File decrypted successfully.
document.pdf
```

### Decrypting Steganographic Images

#### Step 1: Select Decryption

From the main menu, select **Decrypt**.

#### Step 2: Choose Image Decryption

Select **Image**:

```
? What do you want to decrypt?
  Text
  File
❯ Image
```

#### Step 3: Provide Image Path

Enter the path to the image containing hidden data:

```
? Enter the path of the image to decrypt: /path/to/encrypto.png
```

#### Step 4: Enter Password

Enter the password used to encrypt the hidden message:

```
? Enter password: ••••••••
```

#### Step 5: View Result

The hidden message will be displayed:

```
The decrypted text is: My secret message
```

## Password Requirements

⚠️ **Critical**: You must use the **exact same password** that was used during encryption.

### Important Notes

- **Case-sensitive**: `MyPassword` ≠ `mypassword`
- **Exact match**: No typos allowed
- **No recovery**: If you forget the password, the data cannot be recovered
- **Character-sensitive**: All special characters must be identical

## What Happens If Password Is Wrong

If you enter an incorrect password:

```
Either the key or the input data is wrong.
```

This could mean:
- Wrong password
- Data is corrupted
- Data was encrypted with a different method

## Examples

### Example 1: Decrypt a File

```bash
? What do you want to decrypt? File
? Enter the path to the file: ~/Downloads/report.pdf.encrypto
? Enter password: MySecurePassword123!
File decrypted successfully.
→ ~/Downloads/report.pdf
```

### Example 2: Decrypt a Text Message

```bash
? What do you want to decrypt? Text
? Enter the text to decrypt: gAAAAABl7HdkZvJkA8w...
? Enter password: MySecurePassword123!
The decrypted text is: "Meet me at the secret location"
```

### Example 3: Extract Hidden Message from Image

```bash
? What do you want to decrypt? Image
? Enter the path of the image to decrypt: ~/Pictures/encrypto.png
? Enter password: MySecurePassword123!
The decrypted text is: "Important secret data"
```

## File Organization

When decrypting files:

- **Decrypted file location**: Same directory as the encrypted file
- **Original filename**: Restored automatically
- **Overwrite behavior**: Existing files are overwritten without warning

## Troubleshooting

### "Either the key or the input data is wrong"

Possible solutions:
- Double-check your password (case-sensitive!)
- Ensure you're using the correct file
- Try copying the encrypted text again (might have formatting issues)
- Check if the file is corrupted

### "Can't find the file" error

Solutions:
- Verify the file path is correct
- Check file still exists (not moved or deleted)
- Use absolute paths instead of relative paths
- Ensure you have read permission for the file

### Decryption is taking too long

- This is normal for large files (1 GB might take several minutes)
- Large files require more processing time
- Ensure your system has sufficient resources

## Security Notes

🔒 **Decrypted data is temporary**: Once decrypted, the data is readable on your system.

✅ **Best Practices**:
- Decrypt files only on secure, trusted systems
- Delete decrypted files after use if sensitive
- Avoid decrypting on shared computers
- Keep encrypted backups of important files
- Test decryption on a copy before deleting originals

## Batch Decryption

Currently, EncryptoCLI decrypts one file at a time. For multiple files:

1. Note the password used
2. Decrypt each file individually
3. Consider scripting if needed (future enhancement)
