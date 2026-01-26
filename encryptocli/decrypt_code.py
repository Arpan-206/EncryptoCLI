"""Decryption handlers."""

from InquirerPy import inquirer
from termcolor import colored

from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb.handler import LSBSteganography


class DecryptionHandler:
    """Handle decryption workflows for text, files, and images."""

    def __init__(self) -> None:
        """Initialize decryption handler with cipher and steganography instances.

        Returns:
            None
        """
        self.cipher = AESCipher()
        self.steg = LSBSteganography()

    def run(self) -> str | None:
        """Prompt for decryption mode and dispatch accordingly.

        Returns:
            str | None: Decrypted content or result message, None if cancelled.
        """
        type_of_data = inquirer.select(
            message="What do you want to decrypt?",
            choices=["Text", "File", "Image"],
        ).execute()

        if not type_of_data:
            return None

        if type_of_data == "File":
            return self._decrypt_file()
        elif type_of_data == "Image":
            return self._decrypt_image()
        else:
            return self._decrypt_text()

    def _decrypt_text(self) -> str | None:
        """Decrypt text provided by the user.

        Returns:
            str | None: Decrypted text or None if cancelled.
        """
        data = inquirer.text(message="Enter the text to decrypt").execute()

        if not data:
            return

        password = self._get_password()
        if not password:
            return None

        decrypted_text = self.cipher.decrypt_text(data, password)
        return decrypted_text

    def _decrypt_file(self) -> str | None:
        """Decrypt a file using the provided password.

        Returns:
            str | None: Success message or None if cancelled.
        """
        file_path = inquirer.text(message="Enter the path to the file").execute()

        if not file_path:
            return

        password = self._get_password()
        if not password:
            return None

        self.cipher.decrypt_file(file_path, password)
        return "File decrypted successfully"

    def _decrypt_image(self) -> str | None:
        """Decrypt text hidden inside an image.

        Returns:
            str | None: Decrypted text or None if cancelled.
        """
        image_path = inquirer.text(
            message="Enter the path of the image to decrypt"
        ).execute()

        if not image_path:
            return

        password = self._get_password()
        if not password:
            return None

        data = self.steg.decrypt_image(image_path)
        decrypted_text = self.cipher.decrypt_text(data, password)
        return decrypted_text

    def _get_password(self) -> str:
        """Prompt the user for a password, returning empty string on cancel.

        Returns:
            str: The password entered by the user, or empty string if cancelled.
        """
        password = inquirer.secret(message="Enter password").execute()

        return password or ""
