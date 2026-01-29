# LSB Handler

Least Significant Bit steganography for hiding data in images.

## Class: LSBHandler

```python
from encryptocli.steganography.lsb import LSBHandler

handler = LSBHandler()
```

## Methods

### hide(image_path, secret_data, password)

Hide encrypted data in least significant bits of image.

**Parameters:**
- `image_path` (str): Path to PNG image
- `secret_data` (str or bytes): Encrypted data to hide
- `password` (str): Password for data authentication

**Returns:** bytes - Modified image with hidden data

**Raises:**
- `FileOperationError` - If image cannot be read
- `InvalidInputError` - If data too large for image

**Example:**
```python
handler = LSBHandler()
encrypted = "encrypted_message_here"
hidden_image = handler.hide("photo.png", encrypted, "password123")

# Save modified image
with open("output.png", "wb") as f:
    f.write(hidden_image)
```

### extract(image_path, password)

Extract and verify hidden data from image.

**Parameters:**
- `image_path` (str): Path to image with hidden data
- `password` (str): Password used during hiding

**Returns:** str or bytes - Extracted hidden data

**Raises:**
- `FileOperationError` - If image cannot be read
- `InvalidInputError` - If no valid hidden data found
- `ValueError` - If password verification fails

**Example:**
```python
handler = LSBHandler()
hidden_data = handler.extract("output.png", "password123")
print(hidden_data)
```

### get_capacity(image_path)

Calculate maximum data capacity for image.

**Parameters:**
- `image_path` (str): Path to PNG image

**Returns:** int - Maximum bytes that can be hidden

**Example:**
```python
handler = LSBHandler()
capacity = handler.get_capacity("photo.png")
print(f"Can hide up to {capacity} bytes")
```

## How LSB Works

### Encoding Process

1. Convert secret data to binary
2. Calculate data length (need header)
3. Verify data fits in image
4. Iterate through image pixels
5. Replace LSB of each channel with data bits
6. Recipient sees no visual change

### Decoding Process

1. Extract LSB from each pixel channel
2. Read length header
3. Extract data bits based on length
4. Verify password/checksum
5. Return original data

## Data Format

Hidden data structure:

```
[Header] [Data] [Checksum]

Header (2 bytes): Data length
Data (N bytes): Encrypted data
Checksum (4 bytes): CRC32 for verification
```

## Capacity

Capacity depends on image dimensions and color channels. Larger images can hold more data. Use `get_capacity()` method to determine exact capacity for your image.

## Usage Examples

### Hide Text Message

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb import LSBHandler

# Encrypt the message
cipher = AESCipher()
encrypted = cipher.encrypt("Meet at the place", "secret_pass")

# Hide in image
handler = LSBHandler()
hidden_image = handler.hide("photo.png", encrypted, "secret_pass")

# Save
with open("secret_photo.png", "wb") as f:
    f.write(hidden_image)
```

### Extract Hidden Message

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb import LSBHandler

# Extract from image
handler = LSBHandler()
encrypted = handler.extract("secret_photo.png", "secret_pass")

# Decrypt the message
cipher = AESCipher()
message = cipher.decrypt(encrypted, "secret_pass")
print(message)
```

### Check Image Capacity

```python
from encryptocli.steganography.lsb import LSBHandler

handler = LSBHandler()

# Check if data fits
image_path = "photo.png"
data = "This is the secret message"
capacity = handler.get_capacity(image_path)

print(f"Image capacity: {capacity} bytes")
print(f"Data size: {len(data)} bytes")
print(f"Fits: {len(data) <= capacity}")
```

### Hide File Data

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb import LSBHandler

# Read and encrypt file
with open("secret.txt", "rb") as f:
    data = f.read()

cipher = AESCipher()
encrypted = cipher.encrypt(data.decode('utf-8'), "password")

# Hide in image
handler = LSBHandler()
hidden_image = handler.hide("large_photo.png", encrypted, "password")

with open("secret_photo.png", "wb") as f:
    f.write(hidden_image)
```

## Complexity

### Time Complexity

- Hiding: O(W * H) - linear with image size
- Extraction: O(W * H) - linear with image size

### Space Complexity

- O(W * H * 3) - image data in memory

## Error Handling

```python
from encryptocli.steganography.lsb import LSBHandler
from encryptocli.util.exceptions import (
    FileOperationError,
    InvalidInputError
)

handler = LSBHandler()

try:
    # Try to hide data larger than capacity
    hidden = handler.hide("small.png", "large_data" * 1000, "pass")
except InvalidInputError as e:
    print(f"Data too large: {e}")

try:
    # Extract with wrong password
    data = handler.extract("hidden.png", "wrong_pass")
except ValueError as e:
    print(f"Password verification failed: {e}")

try:
    # Image file issue
    data = handler.extract("missing.png", "pass")
except FileOperationError as e:
    print(f"Cannot read image: {e}")
```

## Security Considerations

### Strengths

- Data completely hidden
- No visual artifacts
- Simple and efficient
- Good capacity

### Weaknesses

- Detectable with steganalysis
- No compression
- Sensitive to image modification
- Any pixel change loses data

### Best Practices

1. Use with encryption (LSB + AES)
2. Select unremarkable images
3. Don't share suspiciously
4. Keep passwords secure
5. Backup hidden images

## Image Requirements

### Supported Format

- **Format**: PNG only (lossless)
- **Channels**: RGB (preferred) or RGBA
- **Bit Depth**: 8-bit per channel

### Image Quality

- Original photo best
- Avoid computer-generated images
- Avoid images with gradients
- Natural images preferred

## Limitations

- PNG format only (no JPEG)
- Cannot hide more than capacity
- Any image modification loses data
- Password must be remembered
- No built-in compression

## Comparison with DCT

| Feature | LSB | DCT |
|---------|-----|-----|
| Algorithm | Spatial domain | Frequency domain |
| Capacity | Higher | Lower |

## See Also

- [DCT Handler](dct_handler.md)
- [Steganography Overview](index.md)
- [Services - EncryptionService](../services.md)
