"""Core decryption business logic service."""

from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb.handler import LSBSteganography


class DecryptionService:
    """Handle decryption logic without UI dependencies."""

    def __init__(self) -> None:
        """Initialize decryption service with cipher and steganography instances.

        Returns:
            None
        """
        self.cipher = AESCipher()
        self.steg = LSBSteganography()

    def decrypt_text(self, data: str, password: str) -> str:
        """Decrypt text.

        Args:
            data: The encrypted text to decrypt
            password: The password used for encryption

        Returns:
            str: The decrypted text
        """
        return self.cipher.decrypt_text(data, password)

    def decrypt_file(self, file_path: str, password: str) -> str:
        """Decrypt a file.

        Args:
            file_path: Path to the encrypted file
            password: The password used for encryption

        Returns:
            str: Success message
        """
        self.cipher.decrypt_file(file_path, password)
        return "File decrypted successfully"

    def decrypt_image(self, image_path: str, password: str) -> str:
        """Decrypt text hidden inside an image.

        Args:
            image_path: Path to the image file containing encrypted text
            password: The password used for encryption

        Returns:
            str: The decrypted text
        """
        data = self.steg.decrypt_image(image_path)
        decrypted_text = self.cipher.decrypt_text(data, password)
        return decrypted_text
