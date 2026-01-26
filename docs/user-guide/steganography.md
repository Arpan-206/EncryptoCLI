# Steganography Guide

Steganography is the art of hiding information within other information. In EncryptoCLI, you can use LSB (Least Significant Bit) steganography to hide encrypted messages inside images.

## What is Steganography?

Steganography hides data so that it's undetectable by anyone looking at the image. Unlike encryption (which scrambles data), steganography **conceals the very existence** of the data.

### Key Differences

| Aspect | Encryption | Steganography |
|--------|------------|---------------|
| **Visibility** | Obviously encrypted | Invisible to the naked eye |
| **Detection** | Obvious something is hidden | Hidden presence of data |
| **Purpose** | Protect information | Conceal existence of information |
| **Combined** | Encryption + Steganography = Maximum security |

## How LSB Steganography Works

LSB (Least Significant Bit) steganography works by:

1. **Converting message** to binary (1s and 0s)
2. **Replacing** the least significant bits of image pixels
3. **Result**: Imperceptible changes to image appearance
4. **Advantage**: Maximum data while minimizing image distortion

### Visual Example

```
Original pixel RGB:  (242, 156, 80)  → Binary: ...00000, ...11100, ...00000
After hiding data:   (242, 157, 81)  → Binary: ...00000, ...11101, ...00001
Visual difference:   Completely invisible to human eyes
```

## Supported Image Formats

### Best Formats

| Format | Recommended | Notes |
|--------|-----------|-------|
| **PNG** | ✅ Yes | Best choice - lossless compression |
| **BMP** | ✅ Yes | Works well, larger file sizes |
| **TIFF** | ✅ Yes | Good for archival |
| **JPEG** | ❌ No | Lossy compression destroys hidden data |
| **GIF** | ⚠️ Limited | May work with some versions |

**Recommendation**: Always use PNG format for steganography with EncryptoCLI.

## Hiding Encrypted Data in Images

### Step 1: Select Encryption

From the main menu, select **Encrypt**.

### Step 2: Choose Text Encryption

Select **Text**:

```
? What do you want to encrypt?
❯ Text
  File
```

### Step 3: Choose Image Output

Select **Image**:

```
? What do you want to encrypt to?
❯ Image
  Text
```

### Step 4: Provide Image Path

Enter the path to your image file:

```
? Enter the path to the image. ( PNG file recommended ): /path/to/vacation.png
```

### Step 5: Enter Secret Message

Type the message you want to hide:

```
? Enter the text to encrypt: "Secret meeting location: coordinates 40.7128, -74.0060"
```

### Step 6: Enter Password

Create a password to protect the hidden message:

```
? Enter the password: MySecurePassword123!
```

### Step 7: Done

The image with hidden data is saved as `encrypto.png`:

```
→ encrypto.png
```

The original image is **unchanged**, and visually identical to the original.

## Extracting Hidden Data from Images

### Step 1: Select Decryption

From the main menu, select **Decrypt**.

### Step 2: Choose Image Decryption

Select **Image**:

```
? What do you want to decrypt?
  Text
  File
❯ Image
```

### Step 3: Provide Image Path

Enter the path to the steganographic image:

```
? Enter the path of the image to decrypt: /path/to/encrypto.png
```

### Step 4: Enter Password

Enter the password used to encrypt the message:

```
? Enter password: MySecurePassword123!
```

### Step 5: View Hidden Message

The decrypted message will be displayed:

```
The decrypted text is: "Secret meeting location: coordinates 40.7128, -74.0060"
```

## Use Cases

### Secure Communication
Share images on public social media with hidden encrypted messages that only intended recipients can read.

### Data Protection
Hide sensitive information within innocent-looking images.

### Digital Watermarking
Embed metadata or copyright information imperceptibly.

### Confidential Storage
Store secrets in image collections without raising suspicion.

### Covert Operations
Communicate without revealing that any communication is occurring.

## Capacity Limitations

The amount of data you can hide depends on image size:

| Image Size | Max Data | Notes |
|-----------|----------|-------|
| 100x100 px | ~3.6 KB | Small images have limited capacity |
| 500x500 px | ~90 KB | Moderate capacity |
| 1000x1000 px | ~364 KB | Good capacity |
| 2000x2000 px | ~1.5 MB | Large capacity |
| 4000x4000 px | ~6 MB | Very large capacity |

**Formula**: Approximate capacity = (Width × Height) / 32 bytes

## Best Practices

✅ **Do**:
- Use PNG format
- Use high-resolution images (larger capacity)
- Create backups of original images
- Use strong passwords
- Test on a copy first
- Document hidden messages for your own reference

❌ **Don't**:
- Use JPEG format (data will be corrupted)
- Hide extremely sensitive data without encryption
- Share the image on platforms that re-compress images
- Assume visual similarity means no data loss
- Forget the password
- Edit the image after hiding data (will corrupt hidden data)

## Security Considerations

### Strength of Concealment

LSB steganography provides:
- **Visual security**: Hidden data is invisible to the eye
- **Not format-compatible**: Works only with PNG and similar formats
- **Vulnerable to**: Steganalysis (specialized detection methods)

### Recommended Approach: Defense in Depth

For maximum security, combine techniques:

```
Plaintext Message
    ↓
[Encryption with strong password]
    ↓
Encrypted message
    ↓
[LSB Steganography in PNG]
    ↓
Normal-looking image with hidden encrypted data
```

This ensures:
1. **Encryption** protects the data if discovered
2. **Steganography** prevents discovery in the first place
3. **Combined**: Multi-layer protection

## Troubleshooting

### "Image not found" error
- Verify the file path
- Use absolute paths
- Ensure file has correct extension (.png)

### Hidden data appears corrupted
- Original image was edited after hiding data
- Image was converted to different format (especially JPEG)
- Original image file was corrupted

### Message size too large for image
- Use a larger image
- Use multiple images for the same message
- Compress the message first

### Image looks different after hiding data
- LSB changes should be invisible
- If visible, there may be an issue with the image format
- Try a different image

## Examples

### Example 1: Hide a Secret Code

```bash
? What do you want to encrypt? Text
? What do you want to encrypt to? Image
? Enter the path to the image: ~/vacation.png
? Enter the text to encrypt: "OPERATION COMPLETE - RENDEZVOUS AT 0900"
? Enter the password: Operation7#Alpha
→ encrypto.png
```

### Example 2: Extract Secret Code

```bash
? What do you want to decrypt? Image
? Enter the path of the image to decrypt: ~/encrypto.png
? Enter password: Operation7#Alpha
The decrypted text is: "OPERATION COMPLETE - RENDEZVOUS AT 0900"
```

### Example 3: Hide Contact Information

```bash
? What do you want to encrypt? Text
? What do you want to encrypt to? Image
? Enter the path to the image: ~/profile_pic.png
? Enter the text to encrypt: "backup_email: secure@example.com | phone: +1-555-0123"
? Enter the password: ContactBackup#2024
→ encrypto.png
```

## Advanced Topics

### Image Steganalysis

Attackers use specialized tools to detect hidden data in steganographic images. To minimize detection:

- Use high-quality images
- Use larger images relative to data size
- Mix steganography with regular use patterns
- Don't encrypt the image after hiding data

### Format Compatibility

Different image formats handle LSB steganography differently:

- **PNG**: Perfect (lossless)
- **BMP**: Good (uncompressed)
- **TIFF**: Good (lossless)
- **JPEG**: Fails (lossy compression)

### Legal Considerations

Check local laws before using steganography:
- Legal in most countries for personal use
- May be restricted in some jurisdictions
- Consider purpose and context
- Document usage for legitimate purposes
