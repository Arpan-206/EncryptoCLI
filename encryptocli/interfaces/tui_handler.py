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
            "Secure CLI for hashing, encryption, and steganography"
            " (AES/Fernet and PGP).",
            "cyan",
        )
        print(colored(f.renderText("Encrypto CLI"), "green"), credit, description, "\n")

    def get_operation(self) -> str:
        """Prompt the user to choose an operation.

        Returns:
            str: The selected operation ('Hash', 'Encrypt', 'Decrypt',
                'PGP', or 'Exit').
        """
        operation = inquirer.select(
            message="What do you want to do?",
            choices=["Hash", "Encrypt", "Decrypt", "PGP Keys", "Exit"],
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
            elif operation == "PGP Keys":
                self._handle_pgp_keys()
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
        encryption_method = inquirer.select(
            message="Which encryption method do you want to use?",
            choices=["AES (Fernet)", "PGP"],
        ).execute()

        if not encryption_method:
            return

        method = "aes" if encryption_method == "AES (Fernet)" else "pgp"

        use_steganography = inquirer.select(
            message="How do you want to save the encrypted text?",
            choices=["As encrypted text", "Hide in image (Steganography)"],
        ).execute()

        if not use_steganography:
            return

        steganography_type = "lsb"  # Default
        input_image_path = None
        if use_steganography == "Hide in image (Steganography)":
            steganography_type = inquirer.select(
                message="Which steganography method do you want to use?",
                choices=["LSB", "DCT"],
            ).execute()

            if not steganography_type:
                return

            input_image_path = inquirer.text(
                message="Enter the path to the image. ( PNG file recommended )"
            ).execute()
            if not input_image_path:
                return

        secret = inquirer.text(message="Enter the text to encrypt:").execute()
        if not secret:
            return

        if method == "pgp":
            recipient = inquirer.text(
                message="Enter recipient email address:"
            ).execute()
            if not recipient:
                return
            password = recipient
        else:
            password = self._get_password()
            if not password:
                return

        if use_steganography == "As encrypted text":
            result = self.encryption_service.encrypt_text(secret, password, method)
            print(
                colored("The encrypted text is: ", "white") + colored(result, "green")
            )
        else:
            result = self.encryption_service.encrypt_text_to_image(
                str(input_image_path),
                secret,
                password,
                steganography=steganography_type.lower(),
                method=method,
            )
            print(colored(result, "green"))

    def _encrypt_file_tui(self) -> None:
        """Handle file encryption with TUI prompts."""
        encryption_method = inquirer.select(
            message="Which encryption method do you want to use?",
            choices=["AES (Fernet)", "PGP"],
        ).execute()

        if not encryption_method:
            return

        method = "aes" if encryption_method == "AES (Fernet)" else "pgp"

        file_path = inquirer.text(message="Enter the path to the file.").execute()
        if not file_path:
            return

        if method == "pgp":
            password = inquirer.text(message="Enter recipient email address:").execute()
            if not password:
                return
        else:
            password = self._get_password()
            if not password:
                return

        result = self.encryption_service.encrypt_file(file_path, password, method)
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
        decryption_method = inquirer.select(
            message="Which decryption method do you want to use?",
            choices=["AES (Fernet)", "PGP"],
        ).execute()

        if not decryption_method:
            return

        method = "aes" if decryption_method == "AES (Fernet)" else "pgp"

        data = inquirer.text(message="Enter the text to decrypt").execute()
        if not data:
            return

        password = self._get_password()
        if not password:
            return

        result = self.decryption_service.decrypt_text(data, password, method)
        print(colored("The decrypted text is: ", "white") + colored(result, "green"))

    def _decrypt_file_tui(self) -> None:
        """Handle file decryption with TUI prompts."""
        decryption_method = inquirer.select(
            message="Which decryption method do you want to use?",
            choices=["AES (Fernet)", "PGP"],
        ).execute()

        if not decryption_method:
            return

        method = "aes" if decryption_method == "AES (Fernet)" else "pgp"

        file_path = inquirer.text(message="Enter the path to the file").execute()
        if not file_path:
            return

        password = self._get_password()
        if not password:
            return

        output_dir = "./decrypted/" if method == "pgp" else "./"
        result = self.decryption_service.decrypt_file(
            file_path, password, method, output_dir
        )
        print(colored(result, "green"))

    def _decrypt_image_tui(self) -> None:
        """Handle image decryption with TUI prompts."""
        decryption_method = inquirer.select(
            message="Which decryption method was used?",
            choices=["AES (Fernet)", "PGP"],
        ).execute()

        if not decryption_method:
            return

        method = "aes" if decryption_method == "AES (Fernet)" else "pgp"

        steganography_type = inquirer.select(
            message="Which steganography method was used?",
            choices=["LSB", "DCT"],
        ).execute()

        if not steganography_type:
            return

        image_path = inquirer.text(
            message="Enter the path of the image to decrypt"
        ).execute()
        if not image_path:
            return

        password = self._get_password()
        if not password:
            return

        result = self.decryption_service.decrypt_image(
            image_path, password, steganography_type.lower(), method
        )
        print(colored("The decrypted text is: ", "white") + colored(result, "green"))

    def _get_password(self) -> str:
        """Prompt the user for a password.

        Returns:
            str: The password entered by the user, or empty string if cancelled.
        """
        password = inquirer.secret(message="Enter the password: ").execute()
        return password or ""

    def _handle_pgp_keys(self) -> None:
        """Handle PGP key management operations."""
        operation = inquirer.select(
            message="What would you like to do with PGP keys?",
            choices=[
                "Generate Key Pair",
                "List Keys",
                "Import Public Key",
                "Export Public Key",
            ],
        ).execute()

        if not operation:
            return

        try:
            if operation == "Generate Key Pair":
                self._pgp_generate_key()
            elif operation == "List Keys":
                self._pgp_list_keys()
            elif operation == "Import Public Key":
                self._pgp_import_key()
            elif operation == "Export Public Key":
                self._pgp_export_key()
        except Exception as e:
            handle_error(e)

    def _pgp_generate_key(self) -> None:
        """Generate a new PGP key pair."""
        from encryptocli.encryption.pgp import PGPCipher

        name = inquirer.text(message="Enter your full name:").execute()
        if not name:
            return

        email = inquirer.text(message="Enter your email address:").execute()
        if not email:
            return

        passphrase = inquirer.secret(
            message="Enter a passphrase to protect your key:"
        ).execute()
        if not passphrase:
            return

        pgp = PGPCipher()
        fingerprint = pgp.generate_key_pair(name, email, passphrase)

        print(colored("\n✓ PGP Key Generated Successfully!", "green"))
        print(colored(f"Name: {name}", "cyan"))
        print(colored(f"Email: {email}", "cyan"))
        print(colored(f"Fingerprint: {fingerprint}", "yellow"))
        print()

    def _pgp_list_keys(self) -> None:
        """List all available PGP keys."""
        from encryptocli.encryption.pgp import PGPCipher

        pgp = PGPCipher()
        keys = pgp.list_keys()

        if not keys:
            print(colored("No keys found in keyring.", "yellow"))
            return

        print(colored("\n=== PGP Keys ===\n", "cyan"))
        for i, key in enumerate(keys, 1):
            keyid = key.get("keyid", "N/A")
            fingerprint = key.get("fingerprint", "N/A")
            uids = key.get("uids", ["N/A"])

            print(colored(f"{i}. {uids[0]}", "green"))
            print(f"   Key ID: {keyid}")
            print(f"   Fingerprint: {fingerprint}")
            print()

    def _pgp_import_key(self) -> None:
        """Import a public key from a file."""
        from encryptocli.encryption.pgp import PGPCipher

        key_path = inquirer.text(
            message="Enter the path to the public key file (.asc):"
        ).execute()
        if not key_path:
            return

        pgp = PGPCipher()
        result = pgp.import_public_key(key_path)

        print(colored("\n✓ " + result, "green"))
        print()

    def _pgp_export_key(self) -> None:
        """Export a public key to a file."""
        from encryptocli.encryption.pgp import PGPCipher

        email = inquirer.text(
            message="Enter the email address of the key to export:"
        ).execute()
        if not email:
            return

        output_path = inquirer.text(
            message="Enter output file path (default: public_key.asc):",
            default="public_key.asc",
        ).execute()

        pgp = PGPCipher()
        result = pgp.export_public_key(email, output_path)

        print(colored("\n✓ " + result, "green"))
        print()
