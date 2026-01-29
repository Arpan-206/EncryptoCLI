# Steganography

Hide encrypted data inside images using LSB or DCT steganography.

## Overview

Steganography hides data within other data. EncryptoCLI combines encryption with steganography to hide encrypted secrets in image files. The image looks normal but contains hidden encrypted information.

## Steganography Methods

### LSB (Least Significant Bit)

Replaces the least significant bits of image pixels with encrypted data.

- **Advantages**:
  - Simple and fast
  - Works with any PNG image
  - Good capacity

- **Disadvantages**:
  - More detectable with analysis tools
  - Lower security against steganalysis

- **Best For**: Personal files, casual hiding

### DCT (Discrete Cosine Transform)

Embeds data in the frequency domain of the image.

- **Advantages**:
  - More robust against detection
  - Better resistance to image compression
  - Higher security

- **Disadvantages**:
  - Slightly slower processing
  - More complex algorithm

- **Best For**: High-security applications, long-term storage

## Encrypt and Hide Data

### From Text

1. Launch EncryptoCLI: `encryptocli`
2. Select "Encrypt" operation
3. Choose "Image" as output type
4. Enter path to PNG image
5. Choose encryption method (AES or PGP):
   - **AES**: Enter password
   - **PGP**: Enter recipient email
6. Choose steganography method (LSB or DCT)
7. Enter text to hide
8. Encrypted and hidden data in image
9. Result saved as `encryptocli.png`
10. Original image appearance unchanged

### From File

1. Launch EncryptoCLI: `encryptocli`
2. Select "Encrypt" operation
3. Choose "Image" as output type
4. Enter path to PNG image
5. Choose encryption method and password/email
6. Choose steganography method
7. Enter file path to encrypt and hide
8. Encrypted file hidden in image
9. Result saved as `encryptocli.png`

## Extract and Decrypt Data

1. Launch EncryptoCLI: `encryptocli`
2. Select "Decrypt" operation
3. Choose "Image" as data type
4. Enter path to image containing hidden data
5. Enter password (for AES)
6. Select steganography method used (LSB or DCT)
7. View extracted and decrypted data

## Image Requirements

- **Format**: PNG (lossless compression)
- **Size**: Must be large enough to contain encrypted data
  - Larger images = more data can be hidden
- **Quality**: High quality images work best

## Capacity Guide

Capacity depends on your image size. Use the application to check the exact capacity available for your image.

## Security Considerations

- **Encryption**: Data is encrypted before hiding, providing two layers of security
- **Password**: Strong passwords are critical
- **Image Selection**: Use unremarkable images that don't attract attention
- **File Sharing**: Steganalysis tools can potentially detect hidden data
- **Best Practice**: Don't rely solely on steganography; encryption is essential

## Use Cases

- Hide confidential documents in ordinary-looking images
- Secretly share sensitive files
- Create backup copies of encrypted data
- Protect data with visual plausible deniability
- Secure file transfer in restricted environments

## Limitations

- Cannot hide data larger than image capacity
- Recipient must know file contains steganography
- Recipient must have encryption password/keys
- Some image processing (compression, rotation) may corrupt hidden data
