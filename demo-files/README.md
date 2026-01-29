# Demo Files for EncryptoCLI

Sample files for testing EncryptoCLI functionality.

## Files

- `secret_message.txt` - Text message for encryption
- `sample_data.txt` - Structured data (names, emails, etc.)
- `credentials.txt` - Sample credentials
- `sample.bin` - Binary data
- `photo.png` - Image for steganography

## Commands

Run from this directory with `uv run`:

### Encryption & Decryption

```bash
# Encrypt file with AES
uv run encryptocli encrypt --file secret_message.txt --password "pass123" --method aes

# Decrypt file
uv run encryptocli decrypt --file secret_message.txt.encrypto --password "pass123" --method aes

# Encrypt text directly
uv run encryptocli encrypt --text "secret data" --password "pass123" --method aes
```

### Hashing

```bash
# Hash file
uv run encryptocli hash --file sample_data.txt --algorithm SHA256

# Hash with different algorithm
uv run encryptocli hash --file credentials.txt --algorithm BLAKE3

# Hash text
uv run encryptocli hash --text "data" --algorithm SHA256
```

### Steganography - LSB

```bash
# Hide text in image
uv run encryptocli encrypt --text "secret" --image photo.png --password "stego" --method aes --steganography lsb --output ./

# Extract from image
uv run encryptocli decrypt --image encrypto.png --password "stego" --method aes --steganography lsb

# Hide file in image
uv run encryptocli encrypt --file secret_message.txt --image photo.png --password "stego" --method aes --steganography lsb --output ./
```

### Steganography - DCT

```bash
# Hide text in image
uv run encryptocli encrypt --text "secret" --image photo.png --password "dct" --method aes --steganography dct --output ./

# Extract from image
uv run encryptocli decrypt --image encrypto.png --password "dct" --method aes --steganography dct
```

## Demo Workflow

1. **Text Encryption**: `uv run encryptocli encrypt --file secret_message.txt --password "demo123" --method aes`
2. **Decryption**: `uv run encryptocli decrypt --file secret_message.txt.encrypto --password "demo123" --method aes`
3. **Hashing**: `uv run encryptocli hash --file sample_data.txt --algorithm SHA256`
4. **LSB Steganography**: `uv run encryptocli encrypt --text "hide me" --image photo.png --password "pass" --method aes --steganography lsb --output ./`
5. **Extract from Image**: `uv run encryptocli decrypt --image encrypto.png --password "pass" --method aes --steganography lsb`

---
**Note**: Algorithm names must be uppercase (SHA256, BLAKE3, etc.). Steganography outputs to `encrypto.png`.

---
**Note**: These files are for demonstration purposes only. Never store real credentials in plaintext!
