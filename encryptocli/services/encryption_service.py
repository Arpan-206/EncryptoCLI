"""Core encryption business logic service."""

from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb.handler import LSBSteganography


class EncryptionService:
    """Handle encryption logic without UI dependencies."""

    def __init__(self) -> None:
        """Initialize encryption service with cipher and steganography instances.

        Returns:
            None
        """
        self.cipher = AESCipher()
        self.steg = LSBSteganography()

    def encrypt_text(self, secret: str, password: str) -> str:
        """Encrypt text to cipher text.

        Args:
            secret: The text to encrypt
            password: The password to use for encryption

        Returns:
            str: The encrypted text
        """
        return self.cipher.encrypt_text(secret, password)

    def encrypt_text_to_image(
        self, image_path: str, secret: str, password: str, output_dir: str = "./"
    ) -> str:
        """Encrypt text and embed it into an image.

        Args:
            image_path: Path to the image file
            secret: The text to encrypt
            password: The password to use for encryption
            output_dir: Output directory for the encrypted image

        Returns:
            str: Success message
        """
        encrypted_text = self.cipher.encrypt_text(secret, password)
        self.steg.encrypt_text(image_path, encrypted_text, output_dir)
        return "Image encrypted and saved successfully"

    def encrypt_file(self, file_path: str, password: str) -> str:
        """Encrypt a file.

        Args:
            file_path: Path to the file to encrypt
            password: The password to use for encryption

        Returns:
            str: Result message
        """
        return self.cipher.encrypt_file(file_path, password)
