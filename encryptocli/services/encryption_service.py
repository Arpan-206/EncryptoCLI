"""Core encryption business logic service."""

from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography import get_steganography_handler


class EncryptionService:
    """Handle encryption logic without UI dependencies."""

    def __init__(self) -> None:
        """Initialize encryption service with cipher instances.

        Returns:
            None
        """
        self.aes_cipher = AESCipher()
        self._pgp_cipher = None  # Lazy initialization

    def _get_pgp_cipher(self):
        """Get PGP cipher instance, initializing lazily if needed.

        Returns:
            PGPCipher: The PGP cipher instance

        Raises:
            OSError: If GPG is not installed on the system
        """
        if self._pgp_cipher is None:
            try:
                from encryptocli.encryption.pgp import PGPCipher

                self._pgp_cipher = PGPCipher()
            except OSError as e:
                raise OSError(
                    f"GPG (GNU Privacy Guard) is not installed on your system. "
                    f"Please install GPG to use PGP encryption. "
                    f"Details: {str(e)}"
                )
        return self._pgp_cipher

    def encrypt_text(self, secret: str, password: str, method: str = "aes") -> str:
        """Encrypt text to cipher text.

        Args:
            secret: The text to encrypt
            password: The password/recipient email to use for encryption
            method: Encryption method ('aes' or 'pgp'). Default: 'aes'

        Returns:
            str: The encrypted text
        """
        if method.lower() == "pgp":
            encrypted: str = self._get_pgp_cipher().encrypt_text(secret, password)
            return encrypted
        return self.aes_cipher.encrypt_text(secret, password)

    def encrypt_text_to_image(
        self,
        image_path: str,
        secret: str,
        password: str,
        output_dir: str = "./",
        steganography: str = "lsb",
        method: str = "aes",
    ) -> str:
        """Encrypt text and embed it into an image using steganography.

        Args:
            image_path: Path to the input image file (PNG recommended).
            secret: The text to encrypt.
            password: The password/recipient email to use for encryption.
            output_dir: Output directory for the encrypted image (default: current directory).
            steganography: Steganography method to use ('lsb' or 'dct'). Default: 'lsb'.
                          PNG format is used for all methods to ensure data integrity.
            method: Encryption method ('aes' or 'pgp'). Default: 'aes'

        Returns:
            str: Success message.
        """
        if method.lower() == "pgp":
            encrypted_text = self._get_pgp_cipher().encrypt_text(secret, password)
        else:
            encrypted_text = self.aes_cipher.encrypt_text(secret, password)
        steg = get_steganography_handler(steganography)
        steg.encrypt_text(image_path, encrypted_text, output_dir)
        return "Image encrypted and saved successfully"

    def encrypt_file(self, file_path: str, password: str, method: str = "aes") -> str:
        """Encrypt a file.

        Args:
            file_path: Path to the file to encrypt
            password: The password/recipient email to use for encryption
            method: Encryption method ('aes' or 'pgp'). Default: 'aes'

        Returns:
            str: Result message
        """
        if method.lower() == "pgp":
            result: str = self._get_pgp_cipher().encrypt_file(file_path, password)
            return result
        return self.aes_cipher.encrypt_file(file_path, password)
