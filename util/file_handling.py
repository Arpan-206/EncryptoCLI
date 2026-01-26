import os
import util.exceptions as exceptions


def get_file(filename):
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

    except Exception as e:
        # Handling exceptions
        raise exceptions.FatalError("Ran into an issue while openng file")
