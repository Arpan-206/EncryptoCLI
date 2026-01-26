"""AES (Fernet) encryption/decryption utilities using a class-based API."""

from typing import BinaryIO

from cryptography.fernet import Fernet

from encryptocli.util.exceptions import FatalError, MildError
from encryptocli.util.file_handling import get_file
from encryptocli.util.key_gen import key_gen


class AESCipher:
    """Provide Fernet-based encryption and decryption for text and files."""

    def encrypt_text(self, secret: str, password: str) -> str:
        """Encrypt plain text with the supplied password and return the cipher text.

        Args:
            secret: Plain text to encrypt.
            password: Password for encryption.

        Returns:
            str: Encrypted ciphertext as a string.

        Raises:
            FatalError: If password is empty.
        """
        if password == "":
            raise FatalError("Please enter a password")

        cipher = self._cipher(password)
        return cipher.encrypt(secret.encode()).decode()

    def decrypt_text(self, encrypted_secret: str, password: str) -> str:
        """Decrypt cipher text with the supplied password and return plain text.

        Args:
            encrypted_secret: Encrypted ciphertext to decrypt.
            password: Password used during encryption.

        Returns:
            str: Decrypted plaintext.

        Raises:
            FatalError: If password is empty or decryption fails (invalid key/data).
        """
        if password == "":
            raise FatalError("Please enter a password")

        cipher = self._cipher(password)
        try:
            return cipher.decrypt(encrypted_secret.encode()).decode()
        except Exception as exc:
            raise FatalError("Either the key or the input data is wrong.") from exc

    def encrypt_file(self, file_path: str, password: str) -> str:
        """Encrypt a file using Fernet encryption with a password-derived key.

        Args:
            file_path: Path to the file to encrypt.
            password: Password for encryption.

        Returns:
            str: Success message.

        Raises:
            FatalError: If password is empty, file too large, encryption fails,
                or write error.
            MildError: If file is already encrypted (.encrypto extension).
        """
        if password == "":
            raise FatalError("Please enter a password")

        cipher: Fernet = self._cipher(password)
        file: BinaryIO = get_file(file_path)

        if "encrypto" in file.name:
            raise MildError("File is already encrypted.")

        try:
            encrypted_data = cipher.encrypt(file.read())
        except Exception as exc:
            raise FatalError("Ran into an issue while encrypting file") from exc

        try:
            with open(f"{file.name}.encrypto", "wb") as write_file:
                write_file.write(encrypted_data)
                return "File encrypted successfully"
        except Exception as exc:
            raise FatalError("Error while writing to file") from exc

    def decrypt_file(self, file_path: str, password: str) -> None:
        """Decrypt a file previously encrypted by this tool.

        Args:
            file_path: Path to the encrypted file.
            password: Password used during encryption.

        Returns:
            None

        Raises:
            FatalError: If password is empty, decryption fails, or write error occurs.
        """
        if password == "":
            raise FatalError("Please enter a password")

        cipher: Fernet = self._cipher(password)
        file: BinaryIO = get_file(file_path)

        try:
            decrypted_data = cipher.decrypt(file.read())
        except Exception as exc:
            raise FatalError("Ran into an issue while decrypting file") from exc

        try:
            with open(file.name.replace(".encrypto", ""), "wb") as write_file:
                write_file.write(decrypted_data)
        except Exception as exc:
            raise FatalError("Ran into an issue while writing to file") from exc

    def _cipher(self, password: str) -> Fernet:
        """Create a Fernet cipher instance for the given password.

        Args:
            password: Password to derive the encryption key from.

        Returns:
            Fernet: Fernet cipher instance ready for encryption/decryption.

        Raises:
            FatalError: If key derivation or cipher creation fails.
        """
        key = key_gen(password)
        try:
            return Fernet(key)
        except Exception as exc:
            raise FatalError("Key Error!") from exc
