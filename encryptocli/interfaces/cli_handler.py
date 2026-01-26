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
    help="EncryptoCLI - A tool to hash or encrypt your data "
    "easily using Fernet Encryption."
)

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
        help="Hashing algorithm (MD5, SHA256, SHA512, BLAKE2, BLAKE2b)",
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
        ..., "--password", "-p", prompt=True, hide_input=True, help="Password"
    ),
    image: Optional[str] = typer.Option(
        None,
        "--image",
        "-i",
        help="Image file to embed encrypted text (PNG recommended)",
    ),
    output_dir: str = typer.Option(
        "./", "--output", "-o", help="Output directory for encrypted image"
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
            result = encryption_service.encrypt_file(file, password)
            typer.echo(colored(result, "green"))
        else:
            if image:
                if not Path(image).exists():
                    typer.echo(colored(f"Error: Image file not found: {image}", "red"))
                    raise typer.Exit(code=1)
                result = encryption_service.encrypt_text_to_image(
                    str(image), str(text), password, output_dir
                )
                typer.echo(colored(result, "green"))
            else:
                result = encryption_service.encrypt_text(str(text), password)
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
        ..., "--password", "-p", prompt=True, hide_input=True, help="Password"
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
            result = decryption_service.decrypt_file(file, password)
            typer.echo(colored(result, "green"))
        elif image:
            if not Path(image).exists():
                typer.echo(colored(f"Error: Image file not found: {image}", "red"))
                raise typer.Exit(code=1)
            result = decryption_service.decrypt_image(image, password)
            typer.echo(colored("Decrypted text: ", "white") + colored(result, "green"))
        else:
            result = decryption_service.decrypt_text(str(text), password)
            typer.echo(colored("Decrypted text: ", "white") + colored(result, "green"))
    except Exception as e:
        handle_error(e)
        raise typer.Exit(code=1)


def get_app() -> typer.Typer:
    """Get the Typer application instance.

    Returns:
        typer.Typer: The CLI application
    """
    return app
