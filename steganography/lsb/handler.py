"""LSB steganography utilities using a class-based API."""

from stegano import lsb


class LSBSteganography:
    """Hide and reveal secrets using least significant bit steganography."""

    def encrypt_text(
        self, input_image_path: str, secret: str, output_dir: str = "./"
    ) -> None:
        """Embed secret text into an image and save as encrypto.png in output_dir."""
        encrypted = lsb.hide(input_image_path, secret)
        encrypted.save(f"{output_dir}encrypto.png")

    def decrypt_image(self, input_image_path: str) -> str:
        """Extract hidden text from an image."""
        return lsb.reveal(input_image_path)
