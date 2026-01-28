"""PGP (Pretty Good Privacy) encryption/decryption utilities using a class-based API."""

from typing import BinaryIO, Optional
import os

try:
    import gnupg
except ImportError:
    raise ImportError(
        "python-gnupg is required for PGP encryption. Install it with: pip install python-gnupg"
    )

from encryptocli.util.exceptions import FatalError, MildError
from encryptocli.util.file_handling import get_file


class PGPCipher:
    """Provide PGP-based encryption and decryption for text and files."""

    def __init__(self, gpg_home: Optional[str] = None) -> None:
        """Initialize PGP cipher with GPG instance.

        Args:
            gpg_home: Optional custom GPG home directory. If not provided,
                     uses ~/.gnupg (the system GPG keyring). Pass a custom path
                     to use an isolated keyring.

        Returns:
            None
        """
        # Use provided GPG home, or fall back to ~/.gnupg (system default)
        if gpg_home is None:
            gpg_home = os.path.expanduser("~/.gnupg")

        # Ensure the GPG home directory exists
        os.makedirs(gpg_home, exist_ok=True, mode=0o700)

        self.gnupg_home = gpg_home
        self.gpg = gnupg.GPG(gnupghome=self.gnupg_home)

    def generate_key_pair(self, name: str, email: str, passphrase: str) -> str:
        """Generate a PGP key pair.

        Args:
            name: Name for the key.
            email: Email for the key.
            passphrase: Passphrase to protect the key.

        Returns:
            str: Key fingerprint.

        Raises:
            FatalError: If key generation fails.
        """
        if not name or not email or not passphrase:
            raise FatalError(
                "Name, email, and passphrase are required for key generation"
            )

        try:
            input_data = self.gpg.gen_key_input(
                name_real=name,
                name_email=email,
                passphrase=passphrase,
                key_type="RSA",
                key_length=2048,
            )
            key = self.gpg.gen_key(input_data)
            if not key.fingerprint:
                raise FatalError("Failed to generate PGP key")
            return str(key.fingerprint)
        except Exception as exc:
            raise FatalError(f"Error generating PGP key: {str(exc)}") from exc

    def encrypt_text(
        self, secret: str, recipient_email: str, passphrase: Optional[str] = None
    ) -> str:
        """Encrypt plain text with the recipient's public key.

        Args:
            secret: Plain text to encrypt.
            recipient_email: Email address of the recipient (must have their public key).
            passphrase: Optional passphrase for the signing key.

        Returns:
            str: Encrypted ciphertext as a string.

        Raises:
            FatalError: If encryption fails or recipient key not found.
        """
        if not secret:
            raise FatalError("Cannot encrypt empty text")
        if not recipient_email:
            raise FatalError("Recipient email is required")

        try:
            encrypted_data = self.gpg.encrypt(
                secret,
                recipient_email,
                always_trust=True,
                sign=None,
            )
            if not encrypted_data.ok:
                raise FatalError(f"Encryption failed: {encrypted_data.status}")
            return str(encrypted_data)
        except Exception as exc:
            raise FatalError(f"Error encrypting text: {str(exc)}") from exc

    def decrypt_text(self, encrypted_secret: str, passphrase: str) -> str:
        """Decrypt cipher text with the supplied passphrase.

        Args:
            encrypted_secret: Encrypted ciphertext to decrypt.
            passphrase: Passphrase for the private key.

        Returns:
            str: Decrypted plaintext.

        Raises:
            FatalError: If passphrase is empty or decryption fails.
        """
        if not passphrase:
            raise FatalError("Passphrase is required for decryption")

        try:
            decrypted_data = self.gpg.decrypt(encrypted_secret, passphrase=passphrase)
            if not decrypted_data.ok:
                raise FatalError(f"Decryption failed: {decrypted_data.status}")
            return str(decrypted_data)
        except Exception as exc:
            raise FatalError(f"Error decrypting text: {str(exc)}") from exc

    def encrypt_file(self, file_path: str, recipient_email: str) -> str:
        """Encrypt a file using the recipient's public key.

        Args:
            file_path: Path to the file to encrypt.
            recipient_email: Email address of the recipient.

        Returns:
            str: Success message.

        Raises:
            FatalError: If encryption fails or file issues occur.
            MildError: If file is already encrypted.
        """
        file: BinaryIO = get_file(file_path)

        if file.name.endswith(".pgp") or file.name.endswith(".gpg"):
            raise MildError("File is already encrypted with PGP.")

        try:
            encrypted_data = self.gpg.encrypt_file(
                file,
                recipient_email,
                always_trust=True,
                output=f"{file.name}.pgp",
            )
            file.close()

            if not encrypted_data.ok:
                raise FatalError(f"Encryption failed: {encrypted_data.status}")
            return "File encrypted successfully"
        except Exception as exc:
            raise FatalError(f"Error encrypting file: {str(exc)}") from exc

    def decrypt_file(
        self, file_path: str, passphrase: str, output_dir: str = "./"
    ) -> str:
        """Decrypt a file previously encrypted with PGP.

        Args:
            file_path: Path to the encrypted file.
            passphrase: Passphrase for the private key.
            output_dir: Output directory for decrypted file.

        Returns:
            str: Success message.

        Raises:
            FatalError: If decryption fails.
        """
        if not passphrase:
            raise FatalError("Passphrase is required for decryption")

        file: BinaryIO = get_file(file_path)

        try:
            output_file = (
                os.path.basename(file.name).replace(".pgp", "").replace(".gpg", "")
            )
            output_path = os.path.join(output_dir, f"decrypted_{output_file}")

            with open(output_path, "wb") as out:
                self.gpg.decrypt_file(file, passphrase=passphrase, output=out)

            file.close()
            return f"File decrypted successfully to {output_path}"
        except Exception as exc:
            raise FatalError(f"Error decrypting file: {str(exc)}") from exc

    def export_public_key(self, email: str, output_path: str) -> str:
        """Export a public key to a file.

        Args:
            email: Email of the key owner.
            output_path: Path where the public key will be saved.

        Returns:
            str: Success message.

        Raises:
            FatalError: If export fails.
        """
        try:
            public_key = self.gpg.export_keys(email)
            if not public_key:
                raise FatalError(f"No public key found for {email}")

            with open(output_path, "w") as f:
                f.write(public_key)
            return f"Public key exported to {output_path}"
        except Exception as exc:
            raise FatalError(f"Error exporting public key: {str(exc)}") from exc

    def import_public_key(self, key_path: str) -> str:
        """Import a public key from a file.

        Args:
            key_path: Path to the public key file.

        Returns:
            str: Success message with key fingerprint.

        Raises:
            FatalError: If import fails.
        """
        try:
            with open(key_path, "r") as f:
                key_data = f.read()

            import_result = self.gpg.import_keys(key_data)
            if import_result.count == 0:
                raise FatalError("Failed to import public key")

            return f"Public key imported successfully. Fingerprint: {import_result.fingerprints[0]}"
        except Exception as exc:
            raise FatalError(f"Error importing public key: {str(exc)}") from exc

    def list_keys(self) -> list:
        """List all available keys in the keyring.

        Returns:
            list: List of key information dictionaries.
        """
        try:
            public_keys = self.gpg.list_keys()
            return public_keys if public_keys else []
        except Exception as exc:
            raise FatalError(f"Error listing keys: {str(exc)}") from exc
