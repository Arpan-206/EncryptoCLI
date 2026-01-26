"""Unified TUI interface handler using InquirerPy."""

from pyfiglet import Figlet
from InquirerPy import inquirer
from termcolor import colored

from encryptocli.error_handler import handle_error
from encryptocli.services import EncryptionService, DecryptionService, HashingService


class TUIHandler:
    """Single unified handler for all TUI interactions."""

    def __init__(self) -> None:
        """Initialize the TUI handler with service instances.

        Returns:
            None
        """
        self.encryption_service = EncryptionService()
        self.decryption_service = DecryptionService()
        self.hashing_service = HashingService()

    def display_banner(self) -> None:
        """Render the application banner.

        Prints the EncryptoCLI welcome banner with styling.

        Returns:
            None
        """
        f = Figlet(font="slant")
        credit = colored(
            "                                                 By Arpan Pandey\n",
            "yellow",
            attrs=["bold"],
        )
        description = colored(
            "A tool to hash or encrypt your data easily using Fernet Encryption."
            " It is very easy and intuitive to use."
            " You can also use this on any type of file below 1GB.",
            "cyan",
        )
        print(colored(f.renderText("Encrypto CLI"), "green"), credit, description, "\n")

    def get_operation(self) -> str:
        """Prompt the user to choose an operation.

        Returns:
            str: The selected operation ('Hash', 'Encrypt', 'Decrypt',
                or 'Exit').
        """
        operation = inquirer.select(
            message="What do you want to do?",
            choices=["Hash", "Encrypt", "Decrypt", "Exit"],
        ).execute()
        return str(operation)

    def run(self) -> None:
        """Run the TUI, dispatching to the correct service handler.

        Displays the banner, prompts for operation, and delegates to
        appropriate service.

        Returns:
            None
        """
        self.display_banner()

        operation = self.get_operation()
        if not operation:
            return

        try:
            if operation == "Hash":
                self._handle_hash()
            elif operation == "Encrypt":
                self._handle_encrypt()
            elif operation == "Decrypt":
                self._handle_decrypt()
            elif operation == "Exit":
                print(colored("goodbye :)", "blue"))
        except Exception as e:
            handle_error(e)

    def _handle_hash(self) -> None:
        """Handle hashing operation through TUI prompts."""
        algorithm = inquirer.select(
            message="Which algorithm do you want to use?",
            choices=self.hashing_service.get_available_algorithms(),
        ).execute()

        if not algorithm:
            return

        type_of_data = inquirer.select(
            message="What do you want to hash?",
            choices=["Text", "File"],
        ).execute()

        if not type_of_data:
            return

        try:
            if type_of_data == "File":
                file_path = inquirer.text(
                    message="Enter the path to the file."
                ).execute()
                if not file_path:
                    return
                result = self.hashing_service.hash_file(file_path, algorithm)
            else:
                text = inquirer.text(message="Enter the text to hash.").execute()
                if not text:
                    return
                result = self.hashing_service.hash_text(text, algorithm)

            print(colored("Your hash is: ", "white") + colored(result, "green"))
        except Exception as e:
            handle_error(e)

    def _handle_encrypt(self) -> None:
        """Handle encryption operation through TUI prompts."""
        type_of_data = inquirer.select(
            message="What do you want to encrypt?",
            choices=["Text", "File"],
        ).execute()

        if not type_of_data:
            return

        try:
            if type_of_data == "File":
                self._encrypt_file_tui()
            else:
                self._encrypt_text_tui()
        except Exception as e:
            handle_error(e)

    def _encrypt_text_tui(self) -> None:
        """Handle text encryption with TUI prompts."""
        type_of_output = inquirer.select(
            message="What do you want to encrypt to?",
            choices=["Image", "Text"],
        ).execute()

        if not type_of_output:
            return

        input_image_path = None
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

        if type_of_output == "Text":
            result = self.encryption_service.encrypt_text(secret, password)
            print(
                colored("The encrypted text is: ", "white") + colored(result, "green")
            )
        else:
            result = self.encryption_service.encrypt_text_to_image(
                str(input_image_path), secret, password
            )
            print(colored(result, "green"))

    def _encrypt_file_tui(self) -> None:
        """Handle file encryption with TUI prompts."""
        file_path = inquirer.text(message="Enter the path to the file.").execute()
        if not file_path:
            return

        password = self._get_password()
        if not password:
            return

        result = self.encryption_service.encrypt_file(file_path, password)
        print(colored(result, "green"))

    def _handle_decrypt(self) -> None:
        """Handle decryption operation through TUI prompts."""
        type_of_data = inquirer.select(
            message="What do you want to decrypt?",
            choices=["Text", "File", "Image"],
        ).execute()

        if not type_of_data:
            return

        try:
            if type_of_data == "File":
                self._decrypt_file_tui()
            elif type_of_data == "Image":
                self._decrypt_image_tui()
            else:
                self._decrypt_text_tui()
        except Exception as e:
            handle_error(e)

    def _decrypt_text_tui(self) -> None:
        """Handle text decryption with TUI prompts."""
        data = inquirer.text(message="Enter the text to decrypt").execute()
        if not data:
            return

        password = self._get_password()
        if not password:
            return

        result = self.decryption_service.decrypt_text(data, password)
        print(colored("The decrypted text is: ", "white") + colored(result, "green"))

    def _decrypt_file_tui(self) -> None:
        """Handle file decryption with TUI prompts."""
        file_path = inquirer.text(message="Enter the path to the file").execute()
        if not file_path:
            return

        password = self._get_password()
        if not password:
            return

        result = self.decryption_service.decrypt_file(file_path, password)
        print(colored(result, "green"))

    def _decrypt_image_tui(self) -> None:
        """Handle image decryption with TUI prompts."""
        image_path = inquirer.text(
            message="Enter the path of the image to decrypt"
        ).execute()
        if not image_path:
            return

        password = self._get_password()
        if not password:
            return

        result = self.decryption_service.decrypt_image(image_path, password)
        print(colored("The decrypted text is: ", "white") + colored(result, "green"))

    def _get_password(self) -> str:
        """Prompt the user for a password.

        Returns:
            str: The password entered by the user, or empty string if cancelled.
        """
        password = inquirer.secret(message="Enter the password: ").execute()
        return password or ""
