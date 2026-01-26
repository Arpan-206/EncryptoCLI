"""Hashing handlers."""

import hashlib
from typing import Any, Callable

from InquirerPy import inquirer
from termcolor import colored


class HashingHandler:
    """Handle hashing workflows for text and files."""

    ALGORITHMS: dict[str, Callable[[], Any]] = {
        "MD5": hashlib.md5,
        "SHA256": hashlib.sha256,
        "SHA512": hashlib.sha512,
        "BLAKE2": hashlib.blake2s,
        "BLAKE2b": hashlib.blake2b,
    }

    def run(self) -> str | None:
        """Prompt for algorithm and data type, then hash accordingly.

        Returns:
            str | None: The hash result or None if cancelled.
        """
        algorithm = inquirer.select(
            message="Which algorithm do you want to use?",
            choices=list(self.ALGORITHMS.keys()),
        ).execute()

        if not algorithm:
            return

        type_of_data = inquirer.select(
            message="What do you want to hash?",
            choices=["Text", "File"],
        ).execute()

        if not type_of_data:
            return

        hash_out = self.ALGORITHMS[algorithm]()

        if type_of_data == "File":
            return self._hash_file(hash_out)
        else:
            return self._hash_text(hash_out)

    def _hash_text(self, hash_out: Any) -> str | None:
        """Hash text provided by the user.

        Args:
            hash_out: Hash object from hashlib with update() and hexdigest() methods.

        Returns:
            str | None: The computed hash or None if cancelled.
        """
        hash_data = inquirer.text(message="Enter data to hash.").execute()

        if not hash_data:
            return None

        hash_out.update(hash_data.encode())
        final_data = hash_out.hexdigest()
        return final_data

    def _hash_file(self, hash_out: Any) -> str | None:
        """Hash a file in chunks to avoid memory overhead.

        Args:
            hash_out: Hash object from hashlib with update() and hexdigest() methods.

        Returns:
            str | None: The computed hash or None if cancelled/error.
        """
        file_name = inquirer.text(message="Enter the path to the file.").execute()

        if not file_name:
            return None

        try:
            with open(file_name, "rb") as file_path:
                chunk = 0
                while chunk != b"":
                    chunk = file_path.read(1024)
                    hash_out.update(chunk)

            final_hash = hash_out.hexdigest()
            return final_hash

        except Exception:
            return "Error: Can't find the file. Please check the name and make sure the extension is present."
