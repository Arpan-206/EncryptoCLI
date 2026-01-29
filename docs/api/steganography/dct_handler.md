# DCT Handler

Discrete Cosine Transform steganography for robust data hiding in images.

## Class: DCTHandler

```python
from encryptocli.steganography.dct import DCTHandler

handler = DCTHandler()
```

## Methods

### hide(image_path, secret_data, password)

Hide encrypted data using DCT frequency domain embedding.

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
handler = DCTHandler()
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
handler = DCTHandler()
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
handler = DCTHandler()
capacity = handler.get_capacity("photo.png")
print(f"Can hide up to {capacity} bytes")
```

## How DCT Works

### Overview

DCT (Discrete Cosine Transform) converts image from spatial domain to frequency domain, similar to JPEG compression.

### Encoding Process

1. Convert image to YCbCr color space
2. Divide into 8x8 blocks
3. Apply DCT to each block
4. Quantize coefficients
5. Embed data in middle-frequency coefficients
6. Apply inverse DCT
7. Convert back to RGB

### Advantages of Frequency Domain

- Robust against compression
- Imperceptible to human vision
- Data survives minor image modifications
- Better than LSB for JPEG-like compression

## Data Format

Hidden data structure:

```
[Header] [Data] [Checksum]

Header (2 bytes): Data length
Data (N bytes): Encrypted data
Checksum (4 bytes): CRC32 for verification
```

## Capacity

Capacity depends on quantization matrix and image dimensions. Use `get_capacity()` method to determine exact capacity for your image. DCT typically provides different capacity characteristics than LSB.

## Usage Examples

### Hide Text Message

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.dct import DCTHandler

# Encrypt the message
cipher = AESCipher()
encrypted = cipher.encrypt("Top secret meeting details", "secure_pass")

# Hide in image using DCT
handler = DCTHandler()
hidden_image = handler.hide("photo.png", encrypted, "secure_pass")

# Save
with open("secure_photo.png", "wb") as f:
    f.write(hidden_image)
```

### Extract Hidden Message

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.dct import DCTHandler

# Extract from image
handler = DCTHandler()
encrypted = handler.extract("secure_photo.png", "secure_pass")

# Decrypt the message
cipher = AESCipher()
message = cipher.decrypt(encrypted, "secure_pass")
print(message)
```

### Compare LSB and DCT Capacity

```python
from encryptocli.steganography.lsb import LSBHandler
from encryptocli.steganography.dct import DCTHandler

image_path = "photo.png"

lsb_handler = LSBHandler()
dct_handler = DCTHandler()

lsb_capacity = lsb_handler.get_capacity(image_path)
dct_capacity = dct_handler.get_capacity(image_path)

print(f"LSB capacity: {lsb_capacity} bytes")
print(f"DCT capacity: {dct_capacity} bytes")
print(f"LSB/DCT ratio: {lsb_capacity/dct_capacity:.2f}")
```

### Hide Large File

```python
from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.dct import DCTHandler

# Read large file
with open("archive.zip", "rb") as f:
    data = f.read()

# Encrypt
cipher = AESCipher()
encrypted = cipher.encrypt(data.decode('latin1'), "password")

# Hide in large image using DCT
handler = DCTHandler()
hidden_image = handler.hide("large_photo.png", encrypted, "password")

with open("archive_hidden.png", "wb") as f:
    f.write(hidden_image)
```

## Complexity

### Time Complexity

- Hiding: O(W * H) - includes DCT computation
- Extraction: O(W * H) - includes inverse DCT

### Space Complexity

- O(W * H * 3) - image data in memory
- O(8 * 8) - DCT block buffers

## Analysis

### Characteristics

- Frequency domain hiding
- Uses DCT transformation
- Different properties than LSB

## Image Handling

### Image Conversion

- Accepts RGB and RGBA PNG
- Converts RGBA to RGB (discards alpha)
- YCbCr conversion for processing
- Converts back to RGB for output

### Quality Preservation

- Uses appropriate quantization
- Minimal visual artifacts
- Preserves image quality
- Output visually identical

## Error Handling

```python
from encryptocli.steganography.dct import DCTHandler
from encryptocli.util.exceptions import (
    FileOperationError,
    InvalidInputError
)

handler = DCTHandler()

try:
    # Try to hide large data
    hidden = handler.hide("photo.png", "x" * 1000000, "pass")
except InvalidInputError as e:
    print(f"Data too large for DCT: {e}")

try:
    # Extract with wrong password
    data = handler.extract("hidden.png", "wrong_pass")
except ValueError as e:
    print(f"Password verification failed: {e}")

try:
    # Corrupted image
    data = handler.extract("corrupted.png", "pass")
except FileOperationError as e:
    print(f"Cannot process image: {e}")
```

## Advanced Usage

### Custom Quantization

```python
# DCT allows customization of quantization
# Higher quantization = lower capacity but more robust
# Lower quantization = higher capacity but less robust
```

### Image Handling

DCT operates in the frequency domain and may be affected by:
- Image compression
- Resizing operations
- Filtering operations
- Color space conversions

## Comparison with LSB

| Feature | LSB | DCT |
|---------|-----|-----|
| Algorithm | Spatial domain | Frequency domain |
| Capacity | Higher | Lower |

## Best Practices

1. Use DCT for security-critical applications
2. Always encrypt data before hiding
3. Use strong passwords
4. Keep hidden images backed up
5. Test extraction before final use
6. Consider image size vs. capacity
7. Use natural photos rather than graphics

## Limitations

- PNG format only
- Lower capacity than LSB
- Slower processing
- Cannot hide more than capacity
- Requires enough image resolution

## See Also

- [LSB Handler](lsb_handler.md)
- [Steganography Overview](index.md)
- [Services - EncryptionService](../services.md)
