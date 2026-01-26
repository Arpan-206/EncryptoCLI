"""Key generation utilities for Fernet encryption."""

import random
from base64 import urlsafe_b64encode
from hashlib import scrypt


def key_gen(passW: str) -> bytes:
    """Generate a cryptographic key from a password using scrypt.

    Args:
        passW: The password to derive a key from.

    Returns:
        bytes: A base64-encoded cryptographic key suitable for Fernet encryption.
    """
    # Using the password itself as a seed to random to keep salt for scrypt consistent across devices and platforms
    random.seed(passW)
    salt = f"{ random.random() }".encode()
    key = urlsafe_b64encode(
        scrypt(passW.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    )

    return key
