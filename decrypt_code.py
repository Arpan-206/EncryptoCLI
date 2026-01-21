"""Decryption handlers."""

from InquirerPy import inquirer
from termcolor import colored

from encryption.aes import AESCipher
from steganography.lsb.handler import LSBSteganography


class DecryptionHandler:
    """Handle decryption workflows for text, files, and images."""

    def __init__(self) -> None:
        self.cipher = AESCipher()
        self.steg = LSBSteganography()

    def run(self) -> None:
        """Prompt for decryption mode and dispatch accordingly."""
        type_of_data = inquirer.select(
            message="What do you want to decrypt?",
            choices=["Text", "File", "Image"],
        ).execute()

        if not type_of_data:
            return

        if type_of_data == "File":
            self._decrypt_file()
        elif type_of_data == "Image":
            self._decrypt_image()
        else:
            self._decrypt_text()

    def _decrypt_text(self) -> None:
        """Decrypt text provided by the user."""
        data = inquirer.text(message="Enter the text to decrypt").execute()

        if not data:
            return

        password = self._get_password()
        if not password:
            return

        decrypted_text = self.cipher.decrypt_text(data, password)
        print(
            colored("The decrypted text is: ", "white")
            + colored(decrypted_text, "green")
        )

    def _decrypt_file(self) -> None:
        """Decrypt a file using the provided password."""
        file_path = inquirer.text(message="Enter the path to the file").execute()

        if not file_path:
            return

        password = self._get_password()
        if not password:
            return

        self.cipher.decrypt_file(file_path, password)
        print(colored("File decrypted succesfully.", "green"))

    def _decrypt_image(self) -> None:
        """Decrypt text hidden inside an image."""
        image_path = inquirer.text(
            message="Enter the path of the image to decrypt"
        ).execute()

        if not image_path:
            return

        password = self._get_password()
        if not password:
            return

        data = self.steg.decrypt_image(image_path)
        decrypted_text = self.cipher.decrypt_text(data, password)
        print(
            colored("The decrypted text is: ", "white")
            + colored(decrypted_text, "green")
        )

    def _get_password(self) -> str:
        """Prompt the user for a password, returning empty string on cancel."""
        password = inquirer.secret(message="Enter password").execute()

        return password or ""
