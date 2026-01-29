"""Core decryption business logic service."""

from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography import get_steganography_handler


class DecryptionService:
    """Handle decryption logic without UI dependencies."""

    def __init__(self) -> None:
        """Initialize decryption service with cipher instances.

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

    def decrypt_text(self, data: str, password: str, method: str = "aes") -> str:
        """Decrypt text.

        Args:
            data: The encrypted text to decrypt
            password: The password/passphrase used for encryption
            method: Decryption method ('aes' or 'pgp'). Default: 'aes'

        Returns:
            str: The decrypted text
        """
        if method.lower() == "pgp":
            decrypted: str = self._get_pgp_cipher().decrypt_text(data, password)
            return decrypted
        return self.aes_cipher.decrypt_text(data, password)

    def decrypt_file(
        self, file_path: str, password: str, method: str = "aes", output_dir: str = "./"
    ) -> str:
        """Decrypt a file.

        Args:
            file_path: Path to the encrypted file
            password: The password/passphrase used for encryption
            method: Decryption method ('aes' or 'pgp'). Default: 'aes'
            output_dir: Output directory for decrypted file (for PGP only)

        Returns:
            str: Success message
        """
        if method.lower() == "pgp":
            result: str = self._get_pgp_cipher().decrypt_file(
                file_path, password, output_dir
            )
            return result
        self.aes_cipher.decrypt_file(file_path, password)
        return "File decrypted successfully"

    def decrypt_image(
        self,
        image_path: str,
        password: str,
        steganography: str = "lsb",
        method: str = "aes",
    ) -> str:
        """Decrypt text hidden inside an image using steganography.

        Args:
            image_path: Path to the PNG image file containing encrypted text.
            password: The password/passphrase used for encryption.
            steganography: Steganography method to use ('lsb' or 'dct'). Default: 'lsb'.
                          Must match the method used during encryption.
            method: Decryption method ('aes' or 'pgp'). Default: 'aes'

        Returns:
            str: The decrypted text.
        """
        steg = get_steganography_handler(steganography)
        data = steg.decrypt_image(image_path)
        if method.lower() == "pgp":
            result: str = self._get_pgp_cipher().decrypt_text(data, password)
        else:
            result = self.aes_cipher.decrypt_text(data, password)
        return result
