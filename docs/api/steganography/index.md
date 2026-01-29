# Steganography

Hide encrypted data inside images using LSB or DCT methods.

## Overview

Steganography techniques hide data within image files. EncryptoCLI provides two methods:

1. **LSB (Least Significant Bit)** - Simple, fast, good capacity
2. **DCT (Discrete Cosine Transform)** - Secure, robust, lower capacity

## LSB Steganography

Hides data in the least significant bits of pixel values.

### Advantages

- Fast processing
- High data capacity
- Works with any PNG
- Simple algorithm

### Disadvantages

- Detectable with analysis
- No compression
- Sensitive to image modifications

### Usage

```python
from encryptocli.steganography.lsb import LSBHandler

handler = LSBHandler()

# Hide data in image
encrypted_image = handler.hide("image.png", "encrypted_data", "password")

# Extract data from image
extracted = handler.extract("image.png", "password")
```

See [LSB Handler Documentation](lsb_handler.md) for detailed API.

## DCT Steganography

Hides data in frequency domain using Discrete Cosine Transform.

### Advantages

- More secure
- Resistant to compression
- Better visual quality
- Hard to detect

### Disadvantages

- Slower processing
- Lower data capacity
- More complex

### Usage

```python
from encryptocli.steganography.dct import DCTHandler

handler = DCTHandler()

# Hide data in image
encrypted_image = handler.hide("image.png", "encrypted_data", "password")

# Extract data from image
extracted = handler.extract("image.png", "password")
```

See [DCT Handler Documentation](dct_handler.md) for detailed API.

## Selecting a Method

### Use LSB When:

- Speed is important
- Large data capacity needed
- Casual hiding acceptable
- Recipient knows to expect steganography

### Use DCT When:

- Security is critical
- Robustness against detection needed
- Data preservation important
- Professional applications

## Workflow

### Hide Data (Encryption + Steganography)

```python
from encryptocli.services import EncryptionService

service = EncryptionService()

# Encrypt first
encrypted = service.encrypt_text("secret", "password", method="aes")

# Then hide in image
image_with_data = service.encrypt_image(
    "image.png",
    encrypted,
    "password",
    method="aes",
    stego_method="lsb"
)

# Save image
with open("encrypted_image.png", "wb") as f:
    f.write(image_with_data)
```

### Extract Data (Steganography + Decryption)

```python
from encryptocli.services import DecryptionService

service = DecryptionService()

# Extract from image
extracted = service.decrypt_image(
    "encrypted_image.png",
    "password",
    method="aes",
    stego_method="lsb"
)

# Data is already decrypted
print(extracted)
```

## Image Requirements

- **Format**: PNG (lossless)
- **Size**: Large enough for data
- **Quality**: High quality preferred
- **Channels**: RGB or RGBA

## Capacity Considerations

Both LSB and DCT capacity depend on image dimensions. Use the `get_capacity()` method to determine the exact capacity for your specific image.

## Security Considerations

### Steganography Security

- Hides data existence, not data content
- Combined with encryption for security
- No security if existence is suspected
- Detectable with advanced tools

### Best Practices

1. Always encrypt data first
2. Use strong passwords
3. Select unremarkable images
4. Don't share suspiciously
5. DCT for high-security needs

## Implementation Details

### LSB Implementation

- Modifies least significant bit of pixel values
- Red, Green, Blue channels
- Changes imperceptible to human eye
- Linear order encoding

### DCT Implementation

- Frequency domain transformation
- JPEG-like compression concepts
- Quantization table for capacity control
- More robust to compression

## Error Handling

```python
from encryptocli.steganography.lsb import LSBHandler
from encryptocli.util.exceptions import (
    FileOperationError,
    InvalidInputError
)

handler = LSBHandler()

try:
    hidden = handler.hide("image.png", "data", "password")
except InvalidInputError as e:
    print(f"Image too small for data: {e}")
except FileOperationError as e:
    print(f"File error: {e}")
```

## Performance

| Operation | LSB | DCT |
|-----------|-----|-----|
| 1 MB Hide | 100ms | 500ms |
| 1 MB Extract | 100ms | 500ms |
| CPU Usage | Low | Moderate |
| Memory | Low | Moderate |

## Limitations

- Image format must be PNG
- Recipient must know method used
- Data cannot exceed image capacity
- Image processing may corrupt data
- No compression

## See Also

- [LSB Handler](lsb_handler.md)
- [DCT Handler](dct_handler.md)
- [Services - EncryptionService](../services.md)
