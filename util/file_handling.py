import os
from typing import BinaryIO

import util.exceptions as exceptions


def get_file(filename: str) -> BinaryIO:
    """Open and return a file in binary mode after validating its size.

    Args:
        filename: Path to the file to open.

    Returns:
        BinaryIO: File object opened in binary mode.

    Raises:
        FatalError: If file is too large (>1GB) or cannot be opened.
    """
    file_size = os.path.getsize(f"{filename}")

    # Verifying if the file size is less than 1 GB
    if file_size > 1073741824:
        raise exceptions.FatalError(
            "File too large. Only files till 1GB are supported."
        )

    try:
        # Opening and reading the file as binary
        file = open(filename, "rb")
        return file

    except Exception:
        # Handling exceptions
        raise exceptions.FatalError("Ran into an issue while openng file")
