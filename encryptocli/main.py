"""CLI entrypoint for EncryptoCLI."""

from pyfiglet import Figlet
from InquirerPy import inquirer
from termcolor import colored

from encryptocli.decrypt_code import DecryptionHandler
from encryptocli.encrypt_code import EncryptionHandler
from encryptocli.error_handler import handle_error
from encryptocli.hash_code import HashingHandler


class EncryptoCLI:
    """Orchestrates the CLI flow and delegates to feature handlers."""

    def __init__(self) -> None:
        """Initialize the CLI with handler instances.

        Returns:
            None
        """
        self.encryption_handler = EncryptionHandler()
        self.decryption_handler = DecryptionHandler()
        self.hashing_handler = HashingHandler()

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
            str: The selected operation ('Hash', 'Encrypt', 'Decrypt', or 'Exit').
        """
        return inquirer.select(
            message="What do you want to do?",
            choices=["Hash", "Encrypt", "Decrypt", "Exit"],
        ).execute()

    def run(self) -> None:
        """Run the CLI, dispatching to the correct handler.

        Displays the banner, prompts for operation, and delegates to appropriate handler.

        Returns:
            None

        Raises:
            Exception: Caught and displayed via handle_error().
        """
        self.display_banner()

        operation = self.get_operation()
        if not operation:
            return

        try:
            result = None
            if operation == "Hash":
                result = self.hashing_handler.run()
                if result and not result.startswith("Error:"):
                    print(colored("Your hash is: ", "white") + colored(result, "green"))
                elif result:
                    print(colored(result, "red"))
            elif operation == "Encrypt":
                result = self.encryption_handler.run()
                if result:
                    print(
                        colored("The encrypted text is: ", "white")
                        + colored(result, "green")
                    )
            elif operation == "Decrypt":
                result = self.decryption_handler.run()
                if result:
                    print(
                        colored("The decrypted text is: ", "white")
                        + colored(result, "green")
                    )
            elif operation == "Exit":
                print(colored("goodbye :)", "blue"))
            else:
                raise NotImplementedError("operation not supported yet.")
        except Exception as e:
            handle_error(e)


def main() -> None:
    """Legacy entrypoint retained for backward compatibility.

    Returns:
        None
    """
    EncryptoCLI().run()


if __name__ == "__main__":
    main()
