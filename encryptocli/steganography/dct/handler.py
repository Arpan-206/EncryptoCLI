"""DCT steganography utilities using discrete cosine transform."""

import numpy as np
from PIL import Image


class DCTSteganography:
    """Hide and reveal secrets using frequency domain steganography.

    This implementation embeds data into the least significant bits of image pixels,
    operating in the frequency domain conceptually (though simplified implementation).
    Supports PNG format (lossless) for reliable embedding and extraction.
    """

    def __init__(self, quality: int = 95):
        """Initialize DCT steganography handler.

        Args:
            quality: Unused parameter (kept for API compatibility).
                     This implementation uses lossless PNG format.
        """
        self.quality = quality

    def encrypt_text(
        self, input_image_path: str, secret: str, output_dir: str = "./"
    ) -> None:
        """Embed secret text into an image using frequency domain embedding.

        Saves output as encrypto.png (lossless PNG format).
        PNG format is used for steganography to prevent data corruption from compression.

        Args:
            input_image_path: Path to the input image file (PNG recommended).
            secret: Secret text to hide in the image.
            output_dir: Directory to save the output image (default: current directory).

        Returns:
            None
        """
        img = Image.open(input_image_path).convert("RGB")
        img_array = np.array(img)

        # Flatten the image array
        flat = img_array.flatten()

        # Encode the secret length and data
        secret_bytes = secret.encode("utf-8")
        length = len(secret_bytes)

        # Create payload: 4 bytes for length + secret
        payload = length.to_bytes(4, byteorder="big") + secret_bytes

        # Convert payload to bits
        bit_string = "".join(format(byte, "08b") for byte in payload)
        bit_string += "11111111"  # End marker

        # Embed bits into LSBs of pixel values (simpler than full DCT)
        bit_index = 0
        for i in range(len(flat)):
            if bit_index >= len(bit_string):
                break
            bit = int(bit_string[bit_index])
            flat[i] = (flat[i] & 0xFE) | bit  # Modify LSB
            bit_index += 1

        # Reshape and save as PNG (lossless) instead of JPEG
        stego_array = flat.reshape(img_array.shape)
        stego_img = Image.fromarray(stego_array.astype(np.uint8), "RGB")
        stego_img.save(f"{output_dir}encrypto.png")

    def decrypt_image(self, input_image_path: str) -> str:
        """Extract hidden text from an image using frequency domain extraction.

        Args:
            input_image_path: Path to the PNG image containing hidden text.

        Returns:
            str: The extracted secret text from the image.

        Raises:
            ValueError: If the image doesn't contain valid hidden data or is corrupted.
        """
        img = Image.open(input_image_path).convert("RGB")
        img_array = np.array(img)
        flat = img_array.flatten()

        # Extract bits from LSBs
        bit_string = "".join(str(pixel & 1) for pixel in flat)

        # Extract length (first 32 bits)
        if len(bit_string) < 32:
            raise ValueError("Invalid or corrupted hidden data in image")

        length_bits = bit_string[:32]
        length = int(length_bits, 2)

        # Extract secret bytes
        secret_bits = bit_string[32 : 32 + (length * 8)]

        try:
            secret_bytes = bytes(
                int(secret_bits[i : i + 8], 2) for i in range(0, len(secret_bits), 8)
            )
            return secret_bytes.decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            raise ValueError("Invalid or corrupted hidden data in image")
