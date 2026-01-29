# TUI Handler

Interactive Text User Interface using InquirerPy.

## Overview

The TUI provides an interactive menu-driven interface for EncryptoCLI operations.

```bash
encrypto
```

Launches the Text User Interface with guided workflows.

## Main Menu

First screen presents the main operations:

- **Hash** - Generate cryptographic hashes
- **Encrypt** - Protect data with encryption
- **Decrypt** - Recover encrypted data
- **Exit** - Quit the application

## Hash Operation

### Workflow

1. Select "Hash" from main menu
2. Choose data type:
   - Text: Enter text directly
   - File: Provide file path
3. Select hash algorithm from 13 options
4. View generated hash
5. Copy or save result

### Algorithms

- MD5, SHA1 (legacy)
- SHA256, SHA512 (standard)
- SHA3-256, SHA3-512 (modern)
- BLAKE2B, BLAKE3 (fast)
- Additional variants available

## Encrypt Operation

### Workflow

1. Select "Encrypt" from main menu
2. Choose data type:
   - Text: Input directly
   - File: Provide file path
   - Image: Hide in image (steganography)
3. Select encryption method:
   - AES: Password-based
   - PGP: Public key based
4. Provide credentials:
   - AES: Enter password
   - PGP: Enter recipient email
5. (Image only) Select steganography method:
   - LSB: Faster, good capacity
   - DCT: More secure
6. Review and confirm
7. Save encrypted output

### Data Type Details

#### Text Encryption

- Enter text directly in prompt
- Suitable for passwords, messages, notes
- Output shows encrypted text

#### File Encryption

- Enter file path
- Supports all file types
- Output: `encrypto_output.enc`
- Progress indicator for large files

#### Image Encryption

- Enter image path (PNG format)
- Choose steganography method
- Data hidden in image
- Visual appearance unchanged
- Output: `encrypto.png`

### Encryption Methods

#### AES (Password-Based)

- Symmetric encryption
- No setup required
- Password must be strong
- Recipient needs password

#### PGP (Public Key)

- Asymmetric encryption
- Requires GPG installation
- No password needed
- Recipient must be in keyring

## Decrypt Operation

### Workflow

1. Select "Decrypt" from main menu
2. Choose data type:
   - Text: Paste encrypted text
   - File: Provide encrypted file path
   - Image: Extract from image
3. Select decryption method:
   - AES: Enter password
   - PGP: GPG prompts for passphrase
4. (Image only) Select steganography method
5. Confirm decryption
6. View decrypted output

### Data Type Details

#### Text Decryption

- Paste encrypted text
- Enter password/passphrase
- View decrypted result
- Copy decrypted text

#### File Decryption

- Enter encrypted file path
- Enter password/passphrase
- Output: `encrypto_output.dec`
- Restore original file extension

#### Image Decryption

- Enter image path
- Enter password
- Select steganography method
- View hidden decrypted data

## Navigation

### Menu Navigation

- Use arrow keys to move between options
- Press Enter to select
- Type search characters to filter options

### Confirmation Prompts

- Yes/No questions use y/n keys
- Press Enter to confirm
- Type 'q' to go back in some menus

### Cancellation

- Press Ctrl+C to exit at any time
- Unsaved data is lost
- Returns to previous menu or main menu

## Input Validation

### File Paths

- Validated for existence
- Checked for readability
- Shows error if invalid
- Prompts to retry

### Passwords

- Minimum 6 characters
- Typed as asterisks for security
- Confirmed for encryption operations
- Case-sensitive

### Email Addresses (PGP)

- Validated format
- Checked in GPG keyring
- Shows error if not found
- Suggests available keys

### Algorithm Selection

- Shows supported algorithms
- Displays info for each
- Prevents invalid selection
- Remembers last selection

## Error Handling

### Clear Error Messages

```
Error: File not found: /path/to/file.txt
Please enter a valid file path.
```

### Recovery Options

- **Wrong Password**: Retry with correct password
- **File Not Found**: Check path and retry
- **Key Not Found**: Import public key or generate new pair
- **Invalid Input**: Modify input and retry

### Help Information

- Tooltips for each operation
- Algorithm descriptions
- Encryption method comparison
- GPG installation instructions

## Tips and Best Practices

### Efficient Workflow

1. Keep passwords in secure password manager
2. Use same passwords consistently
3. Note file extensions before encryption
4. Verify hash before encryption

### Security

- Always use strong passwords
- Never share private keys
- Keep GPG keys backed up
- Verify recipients before PGP encryption

### Large Files

- Network operations may take time
- Progress shown during operations
- Can interrupt with Ctrl+C
- Partial operations are cleaned up

## Keyboard Shortcuts

- `Up/Down Arrow` - Navigate menu
- `Enter` - Select option
- `Ctrl+C` - Exit/Cancel
- `Ctrl+K` - Clear line (in some inputs)
- `Ctrl+A/E` - Move cursor (in some inputs)

## Output Management

### View Output

- Text appears on screen
- Can be selected and copied
- Long output scrolls

### Save Output

- Option to save after operation
- Choose filename
- Automatic extension added
- Confirmation before overwrite

### Copy to Clipboard

- Not directly supported in TUI
- Can select and copy manually
- Use piping in shell if needed

## Comparison with CLI

| Feature | TUI | CLI |
|---------|-----|-----|
| Learning Curve | Low | Moderate |
| Speed | Slower | Fast |
| Automation | No | Yes |
| Help Available | Yes | Minimal |
| Guided Workflow | Yes | No |
| Suitable For | Manual use | Scripting |

## See Also

- [CLI Handler](cli_handler.md)
- [User Guide](../../user-guide/index.md)
- [Services Documentation](../services.md)
