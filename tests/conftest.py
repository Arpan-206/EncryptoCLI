"""Pytest configuration and shared fixtures."""

import pytest
from PIL import Image
import numpy as np


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_text():
    """Sample text for encryption testing."""
    return "This is a test secret message!"


@pytest.fixture
def sample_password():
    """Sample password for encryption testing."""
    return "test_password_123"


@pytest.fixture
def sample_file(temp_dir):
    """Create a sample text file."""
    file_path = temp_dir / "sample.txt"
    file_path.write_text("Sample file content for testing.")
    return file_path


@pytest.fixture
def sample_image(temp_dir):
    """Create a sample PNG image for steganography."""
    img_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_array, "RGB")
    image_path = temp_dir / "sample.png"
    img.save(image_path)
    return image_path


@pytest.fixture
def large_file(temp_dir):
    """Create a file larger than 1GB limit."""
    file_path = temp_dir / "large.bin"
    # Create a 1.1GB file
    with open(file_path, "wb") as f:
        chunk = b"x" * (1024 * 1024)  # 1MB
        for _ in range(1100):  # 1100MB
            f.write(chunk)
    return file_path
