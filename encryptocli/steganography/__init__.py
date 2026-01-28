"""Steganography module for EncryptoCLI.

Provides multiple steganography methods for hiding data in images:
- LSB (Least Significant Bit): Simple and fast
- DCT (Discrete Cosine Transform): Higher capacity and robustness
"""

from encryptocli.steganography.lsb import LSBSteganography
from encryptocli.steganography.dct import DCTSteganography


def get_steganography_handler(steganography_type: str = "lsb"):
    """Get a steganography handler by type.

    Args:
        steganography_type: Type of steganography handler to use.
            Options: "lsb" (default), "dct"

    Returns:
        An instance of the requested steganography handler.

    Raises:
        ValueError: If steganography_type is not supported.
    """
    handlers = {
        "lsb": LSBSteganography,
        "dct": DCTSteganography,
    }

    if steganography_type not in handlers:
        raise ValueError(
            f"Unknown steganography type: {steganography_type}. "
            f"Supported types: {', '.join(handlers.keys())}"
        )

    return handlers[steganography_type]()


__all__ = ["LSBSteganography", "DCTSteganography", "get_steganography_handler"]
