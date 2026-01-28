"""Core hashing business logic service."""

import hashlib
from pathlib import Path
from typing import Any, Callable

from blake3 import blake3


class HashingService:
    """Handle hashing logic without UI dependencies."""

    ALGORITHMS: dict[str, Callable[[], Any]] = {
        "MD5": hashlib.md5,
        "SHA1": hashlib.sha1,
        "SHA224": hashlib.sha224,
        "SHA256": hashlib.sha256,
        "SHA384": hashlib.sha384,
        "SHA512": hashlib.sha512,
        "SHA3_224": hashlib.sha3_224,
        "SHA3_256": hashlib.sha3_256,
        "SHA3_384": hashlib.sha3_384,
        "SHA3_512": hashlib.sha3_512,
        "BLAKE2S": hashlib.blake2s,
        "BLAKE2B": hashlib.blake2b,
        "BLAKE3": blake3,
    }

    def hash_text(self, text: str, algorithm: str) -> str:
        """Hash text using the specified algorithm.

        Args:
            text: The text to hash
            algorithm: The hashing algorithm to use

        Returns:
            str: The hash digest

        Raises:
            ValueError: If algorithm is not supported
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        hash_obj = self.ALGORITHMS[algorithm]()
        hash_obj.update(text.encode())
        return str(hash_obj.hexdigest())

    def hash_file(self, file_path: str, algorithm: str) -> str:
        """Hash a file using the specified algorithm.

        Args:
            file_path: Path to the file to hash
            algorithm: The hashing algorithm to use

        Returns:
            str: The hash digest

        Raises:
            ValueError: If algorithm is not supported
            FileNotFoundError: If file does not exist
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        hash_obj = self.ALGORITHMS[algorithm]()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return str(hash_obj.hexdigest())

    def get_available_algorithms(self) -> list[str]:
        """Get list of available hashing algorithms.

        Returns:
            list[str]: List of algorithm names
        """
        return sorted(list(self.ALGORITHMS.keys()))
