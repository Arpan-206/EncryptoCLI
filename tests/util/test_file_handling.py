"""Tests for file handling utilities."""

import pytest

from encryptocli.util.file_handling import get_file
from encryptocli.util.exceptions import FatalError


class TestFileHandling:
    """Test file handling utilities."""

    def test_get_file_success(self, sample_file):
        """Test successfully opening a file."""
        file = get_file(str(sample_file))
        assert file is not None
        assert file.readable()
        content = file.read()
        assert b"Sample file content" in content
        file.close()

    def test_get_file_nonexistent(self):
        """Test opening non-existent file raises error."""
        with pytest.raises((FatalError, FileNotFoundError)):
            get_file("/nonexistent/file.txt")

    def test_get_file_too_large(self, temp_dir):
        """Test that files larger than 1GB raise FatalError."""
        # Create a file slightly over 1GB
        large_file = temp_dir / "large.bin"
        size_1gb = 1073741824
        size_over = size_1gb + 1024  # 1GB + 1KB

        with open(large_file, "wb") as f:
            # Write in chunks to avoid memory issues
            chunk_size = 1024 * 1024  # 1MB
            written = 0
            while written < size_over:
                to_write = min(chunk_size, size_over - written)
                f.write(b"x" * to_write)
                written += to_write

        with pytest.raises(FatalError, match="File too large"):
            get_file(str(large_file))

    def test_get_file_binary_mode(self, sample_file):
        """Test that file is opened in binary mode."""
        file = get_file(str(sample_file))
        assert "b" in file.mode
        file.close()
