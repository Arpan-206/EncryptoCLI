"""CLI interface handler using Typer for argument-based interface."""

from pathlib import Path
from typing import Optional

try:
    import typer
except ImportError:
    raise ImportError(
        "Typer is required for CLI mode. Install it with: pip install typer"
    )

from termcolor import colored

from encryptocli.error_handler import handle_error
from encryptocli.services import (
    EncryptionService,
    DecryptionService,
    HashingService,
)

app = typer.Typer(
    help="EncryptoCLI - Secure CLI for hashing, encryption, and steganography "
    "(AES/Fernet and PGP)."
)

# PGP key management subcommands
pgp_app = typer.Typer(help="PGP key management commands")
app.add_typer(pgp_app, name="pgp-key")

# Initialize services
encryption_service = EncryptionService()
decryption_service = DecryptionService()
hashing_service = HashingService()


@app.command()
def hash(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to hash"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="File path to hash"),
    algorithm: str = typer.Option(
        "SHA256",
        "--algorithm",
        "-a",
        help=(
            "Hashing algorithm (e.g., MD5, SHA1, SHA256, SHA512, SHA3_256, "
            "BLAKE2S/B, BLAKE3, ARGON2ID)"
        ),
    ),
) -> None:
    """Hash text or file using specified algorithm."""
    if not text and not file:
        typer.echo(colored("Error: Provide either --text or --file", "red"))
        raise typer.Exit(code=1)

    if text and file:
        typer.echo(colored("Error: Provide either --text or --file, not both", "red"))
        raise typer.Exit(code=1)

    try:
        if file:
            if not Path(file).exists():
                typer.echo(colored(f"Error: File not found: {file}", "red"))
                raise typer.Exit(code=1)
            result = hashing_service.hash_file(file, algorithm)
        else:
            result = hashing_service.hash_text(str(text), algorithm)

        typer.echo(colored(f"Hash ({algorithm}): ", "white") + colored(result, "green"))
    except ValueError as e:
        typer.echo(colored(f"Error: {e}", "red"))
        raise typer.Exit(code=1)
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


@app.command()
def encrypt(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to encrypt"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="File to encrypt"),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        help="Password or recipient email",
    ),
    image: Optional[str] = typer.Option(
        None,
        "--image",
        "-i",
        help="Image file to embed encrypted text (PNG format recommended for steganography)",
    ),
    output_dir: str = typer.Option(
        "./", "--output", "-o", help="Output directory for encrypted image"
    ),
    steganography: str = typer.Option(
        "lsb", "--steganography", "-s", help="Steganography method (lsb, dct)"
    ),
    method: str = typer.Option(
        "aes", "--method", "-m", help="Encryption method (aes, pgp)"
    ),
) -> None:
    """Encrypt text or file."""
    if not text and not file:
        typer.echo(colored("Error: Provide either --text or --file", "red"))
        raise typer.Exit(code=1)

    if text and file:
        typer.echo(colored("Error: Provide either --text or --file, not both", "red"))
        raise typer.Exit(code=1)

    try:
        if file:
            if not Path(file).exists():
                typer.echo(colored(f"Error: File not found: {file}", "red"))
                raise typer.Exit(code=1)
            result = encryption_service.encrypt_file(file, password, method)
            typer.echo(colored(result, "green"))
        else:
            if image:
                if not Path(image).exists():
                    typer.echo(colored(f"Error: Image file not found: {image}", "red"))
                    raise typer.Exit(code=1)
                result = encryption_service.encrypt_text_to_image(
                    str(image), str(text), password, output_dir, steganography, method
                )
                typer.echo(colored(result, "green"))
            else:
                result = encryption_service.encrypt_text(str(text), password, method)
                typer.echo(
                    colored("Encrypted text: ", "white") + colored(result, "green")
                )
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


@app.command()
def decrypt(
    text: Optional[str] = typer.Option(
        None, "--text", "-t", help="Encrypted text to decrypt"
    ),
    file: Optional[str] = typer.Option(
        None, "--file", "-f", help="Encrypted file to decrypt"
    ),
    image: Optional[str] = typer.Option(
        None, "--image", "-i", help="Image file with encrypted text"
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        help="Password or passphrase",
    ),
    steganography: str = typer.Option(
        "lsb", "--steganography", "-s", help="Steganography method (lsb, dct)"
    ),
    method: str = typer.Option(
        "aes", "--method", "-m", help="Decryption method (aes, pgp)"
    ),
    output_dir: str = typer.Option(
        "./", "--output", "-o", help="Output directory for decrypted file"
    ),
) -> None:
    """Decrypt text, file, or image."""
    if not text and not file and not image:
        typer.echo(colored("Error: Provide --text, --file, or --image", "red"))
        raise typer.Exit(code=1)

    provided_count = sum([bool(text), bool(file), bool(image)])
    if provided_count > 1:
        typer.echo(
            colored("Error: Provide only one of --text, --file, or --image", "red")
        )
        raise typer.Exit(code=1)

    try:
        if file:
            if not Path(file).exists():
                typer.echo(colored(f"Error: File not found: {file}", "red"))
                raise typer.Exit(code=1)
            result = decryption_service.decrypt_file(file, password, method, output_dir)
            typer.echo(colored(result, "green"))
        elif image:
            if not Path(image).exists():
                typer.echo(colored(f"Error: Image file not found: {image}", "red"))
                raise typer.Exit(code=1)
            result = decryption_service.decrypt_image(
                image, password, steganography, method
            )
            typer.echo(colored("Decrypted text: ", "white") + colored(result, "green"))
        else:
            result = decryption_service.decrypt_text(str(text), password, method)
            typer.echo(colored("Decrypted text: ", "white") + colored(result, "green"))
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


@pgp_app.command("gen")
def pgp_gen_key(
    name: str = typer.Option(
        ..., "--name", "-n", prompt=True, help="Full name for the key"
    ),
    email: str = typer.Option(
        ..., "--email", "-e", prompt=True, help="Email address for the key"
    ),
    passphrase: str = typer.Option(
        ...,
        "--passphrase",
        "-p",
        prompt=True,
        hide_input=True,
        help="Passphrase to protect the key",
    ),
) -> None:
    """Generate a new PGP key pair (RSA 2048-bit)."""
    try:
        from encryptocli.encryption.pgp import PGPCipher

        pgp = PGPCipher()
        fingerprint = pgp.generate_key_pair(name, email, passphrase)
        typer.echo(colored("PGP Key Generated Successfully!", "green"))
        typer.echo(colored("Fingerprint: ", "white") + colored(fingerprint, "green"))
        typer.echo(colored(f"Email: {email}", "cyan"))
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


@pgp_app.command("export")
def pgp_export_key(
    email: str = typer.Option(
        ..., "--email", "-e", prompt=True, help="Email address of the key to export"
    ),
    output: str = typer.Option(
        "public_key.asc", "--output", "-o", help="Output file path for the public key"
    ),
) -> None:
    """Export a public key to a file."""
    try:
        from encryptocli.encryption.pgp import PGPCipher

        pgp = PGPCipher()
        result = pgp.export_public_key(email, output)
        typer.echo(colored(result, "green"))
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


@pgp_app.command("import")
def pgp_import_key(
    key_file: str = typer.Option(
        ..., "--file", "-f", prompt=True, help="Path to the public key file"
    ),
) -> None:
    """Import a public key from a file."""
    try:
        from encryptocli.encryption.pgp import PGPCipher

        if not Path(key_file).exists():
            typer.echo(colored(f"Error: Key file not found: {key_file}", "red"))
            raise typer.Exit(code=1)

        pgp = PGPCipher()
        result = pgp.import_public_key(key_file)
        typer.echo(colored(result, "green"))
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


@pgp_app.command("list")
def pgp_list_keys() -> None:
    """List all available PGP keys in the keyring."""
    try:
        from encryptocli.encryption.pgp import PGPCipher

        pgp = PGPCipher()
        keys = pgp.list_keys()

        if not keys:
            typer.echo(colored("No keys found in keyring.", "yellow"))
            return

        typer.echo(colored("\n=== PGP Keys ===\n", "cyan"))
        for i, key in enumerate(keys, 1):
            keyid = key.get("keyid", "N/A")
            fingerprint = key.get("fingerprint", "N/A")
            uids = key.get("uids", ["N/A"])
            key_type = key.get("type", "pub")

            typer.echo(colored(f"{i}. {uids[0]}", "green"))
            typer.echo(f"   Type: {key_type}")
            typer.echo(f"   Key ID: {keyid}")
            typer.echo(f"   Fingerprint: {fingerprint}")
            typer.echo()
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


def get_app() -> typer.Typer:
    """Get the Typer application instance.

    Returns:
        typer.Typer: The CLI application
    """
    return app
