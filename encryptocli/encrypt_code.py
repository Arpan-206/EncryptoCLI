"""Encryption handlers."""

from InquirerPy import inquirer
from termcolor import colored

from encryptocli.encryption.aes import AESCipher
from encryptocli.steganography.lsb.handler import LSBSteganography


class EncryptionHandler:
    """Handle encryption workflows for text and files."""

    def __init__(self) -> None:
        """Initialize encryption handler with cipher and steganography instances.

        Returns:
            None
        """
        self.cipher = AESCipher()
        self.steg = LSBSteganography()

    def run(self) -> str | None:
        """Prompt for encryption mode and dispatch to the appropriate handler.

        Returns:
            str | None: Result message or None if cancelled.
        """
        type_of_data = inquirer.select(
            message="What do you want to encrypt?",
            choices=["Text", "File"],
        ).execute()

        if not type_of_data:
            return None

        if type_of_data == "File":
            return self._encrypt_file()
        else:
            return self._encrypt_text()

    def _encrypt_text(self) -> str | None:
        """Encrypt text to either text output or embed into an image.

        Prompts user for output format, image path (if embedding),
        text content, and password.

        Returns:
            str | None: The encrypted text if successful, None if user cancelled or error occurred.
        """
        type_of_output: str | None = inquirer.select(
            message="What do you want to encrypt to?",
            choices=["Image", "Text"],
        ).execute()

        if not type_of_output:
            return

        input_image_path: str | None = None
        if type_of_output == "Image":
            input_image_path = inquirer.text(
                message="Enter the path to the image. ( PNG file recommended )"
            ).execute()
            if not input_image_path:
                return

        secret = inquirer.text(message="Enter the text to encrypt:").execute()

        if not secret:
            return

        password = self._get_password()
        if not password:
            return

        encrypted_text = self.cipher.encrypt_text(secret, password)

        if type_of_output == "Text":
            return encrypted_text

        self.steg.encrypt_text(input_image_path, encrypted_text, "./")
        return "Image encrypted and saved successfully"

    def _encrypt_file(self) -> str | None:
        """Encrypt a file using the provided password.

        Prompts user for file path and password, then encrypts the file.

        Returns:
            str | None: Success message if encrypted, None if user cancelled.
        """
        file_path = inquirer.text(message="Enter the path to the file.").execute()

        if not file_path:
            return

        password = self._get_password()
        if not password:
            return None

        return self.cipher.encrypt_file(file_path, password)

    def _get_password(self) -> str:
        """Prompt the user for a password, returning empty string on cancel.

        Returns:
            str: The password entered by the user, or empty string if cancelled.
        """
        password = inquirer.secret(message="Enter the password: ").execute()

        return password or ""
