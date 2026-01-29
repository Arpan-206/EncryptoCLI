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

    def sign_text(
        self, text: str, passphrase: str, detach: bool = False, clearsign: bool = False
    ) -> str:
        """Sign text with your private key.

        Args:
            text: The text to sign.
            passphrase: Passphrase for your private key.
            detach: If True, create a detached signature (signature separate from data).
            clearsign: If True, create a clear-text signature (readable text with signature).

        Returns:
            str: Signed text or detached signature.

        Raises:
            FatalError: If signing fails.
        """
        if not text:
            raise FatalError("Cannot sign empty text")
        if not passphrase:
            raise FatalError("Passphrase is required for signing")

        try:
            if clearsign:
                signed_data = self.gpg.sign(text, passphrase=passphrase, clearsign=True)
            else:
                signed_data = self.gpg.sign(text, passphrase=passphrase, detach=detach)

            if not signed_data.data:
                raise FatalError(f"Failed to sign text: {signed_data.stderr}")

            return str(signed_data)
        except Exception as exc:
            raise FatalError(f"Error signing text: {str(exc)}") from exc

    def sign_file(self, file_path: str, passphrase: str, detach: bool = True) -> str:
        """Sign a file with your private key.

        Args:
            file_path: Path to the file to sign.
            passphrase: Passphrase for your private key.
            detach: If True, create a detached signature file (.sig).

        Returns:
            str: Path to the signature file or success message.

        Raises:
            FatalError: If signing fails or file not found.
        """
        if not os.path.exists(file_path):
            raise FatalError(f"File not found: {file_path}")
        if not passphrase:
            raise FatalError("Passphrase is required for signing")

        try:
            with open(file_path, "rb") as f:
                signed_data = self.gpg.sign_file(
                    f, passphrase=passphrase, detach=detach
                )

            if not signed_data.data:
                raise FatalError(f"Failed to sign file: {signed_data.stderr}")

            # Save signature to file
            if detach:
                signature_path = f"{file_path}.sig"
                with open(signature_path, "wb") as f:
                    f.write(signed_data.data)
                return f"Detached signature created: {signature_path}"
            else:
                signed_path = f"{file_path}.asc"
                with open(signed_path, "wb") as f:
                    f.write(signed_data.data)
                return f"Signed file created: {signed_path}"
        except Exception as exc:
            raise FatalError(f"Error signing file: {str(exc)}") from exc

    def verify_text(self, signed_text: str) -> dict:
        """Verify a signed text message.

        Args:
            signed_text: The signed text to verify.

        Returns:
            dict: Verification results with keys: valid, fingerprint, username, timestamp.

        Raises:
            FatalError: If verification process fails.
        """
        if not signed_text:
            raise FatalError("Cannot verify empty text")

        try:
            verified = self.gpg.verify(signed_text)

            return {
                "valid": verified.valid,
                "fingerprint": verified.fingerprint,
                "username": verified.username,
                "timestamp": verified.timestamp,
                "trust_level": (
                    verified.trust_text if hasattr(verified, "trust_text") else None
                ),
            }
        except Exception as exc:
            raise FatalError(f"Error verifying text: {str(exc)}") from exc

    def verify_file(self, file_path: str, signature_path: Optional[str] = None) -> dict:
        """Verify a file's signature.

        Args:
            file_path: Path to the file to verify.
            signature_path: Optional path to detached signature file.
                          If not provided, assumes file contains embedded signature.

        Returns:
            dict: Verification results with keys: valid, fingerprint, username, timestamp.

        Raises:
            FatalError: If verification process fails.
        """
        if not os.path.exists(file_path):
            raise FatalError(f"File not found: {file_path}")

        try:
            if signature_path:
                # Verify with detached signature
                if not os.path.exists(signature_path):
                    raise FatalError(f"Signature file not found: {signature_path}")

                with open(file_path, "rb") as f:
                    verified = self.gpg.verify_file(f, signature_path)
            else:
                # Verify embedded signature
                with open(file_path, "rb") as f:
                    verified = self.gpg.verify_file(f)

            return {
                "valid": verified.valid,
                "fingerprint": verified.fingerprint,
                "username": verified.username,
                "timestamp": verified.timestamp,
                "trust_level": (
                    verified.trust_text if hasattr(verified, "trust_text") else None
                ),
            }
        except Exception as exc:
            raise FatalError(f"Error verifying file: {str(exc)}") from exc

    def sign_and_encrypt_text(
        self, text: str, recipient_email: str, passphrase: str
    ) -> str:
        """Sign and encrypt text in one operation.

        Args:
            text: The text to sign and encrypt.
            recipient_email: Email of the recipient (for encryption).
            passphrase: Passphrase for your private key (for signing).

        Returns:
            str: Signed and encrypted text.

        Raises:
            FatalError: If operation fails.
        """
        if not text:
            raise FatalError("Cannot sign and encrypt empty text")
        if not recipient_email:
            raise FatalError("Recipient email is required")
        if not passphrase:
            raise FatalError("Passphrase is required for signing")

        try:
            encrypted_data = self.gpg.encrypt(
                text,
                recipient_email,
                sign=True,
                passphrase=passphrase,
                always_trust=True,
            )

            if not encrypted_data.ok:
                raise FatalError(f"Failed to sign and encrypt: {encrypted_data.stderr}")

            return str(encrypted_data)
        except Exception as exc:
            raise FatalError(f"Error signing and encrypting: {str(exc)}") from exc

    def sign_and_encrypt_file(
        self, file_path: str, recipient_email: str, passphrase: str
    ) -> str:
        """Sign and encrypt a file in one operation.

        Args:
            file_path: Path to the file to sign and encrypt.
            recipient_email: Email of the recipient (for encryption).
            passphrase: Passphrase for your private key (for signing).

        Returns:
            str: Path to the signed and encrypted file.

        Raises:
            FatalError: If operation fails or file not found.
        """
        if not os.path.exists(file_path):
            raise FatalError(f"File not found: {file_path}")
        if not recipient_email:
            raise FatalError("Recipient email is required")
        if not passphrase:
            raise FatalError("Passphrase is required for signing")

        try:
            with open(file_path, "rb") as f:
                encrypted_data = self.gpg.encrypt_file(
                    f,
                    recipient_email,
                    sign=True,
                    passphrase=passphrase,
                    always_trust=True,
                    output=f"{file_path}.pgp",
                )

            if not encrypted_data.ok:
                raise FatalError(
                    f"Failed to sign and encrypt file: {encrypted_data.stderr}"
                )

            return f"File signed and encrypted: {file_path}.pgp"
        except Exception as exc:
            raise FatalError(f"Error signing and encrypting file: {str(exc)}") from exc
