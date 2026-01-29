"""Tests for hashing service."""

import pytest

from encryptocli.services.hashing_service import HashingService


class TestHashingService:
    """Test all hashing algorithms."""

    @pytest.fixture
    def service(self):
        """Provide HashingService instance."""
        return HashingService()

    @pytest.fixture
    def all_algorithms(self, service):
        """Get all available algorithms."""
        return service.get_available_algorithms()

    def test_get_available_algorithms(self, service):
        """Test getting list of available algorithms."""
        algorithms = service.get_available_algorithms()
        assert isinstance(algorithms, list)
        assert len(algorithms) == 13
        assert "SHA256" in algorithms
        assert "MD5" in algorithms
        assert "BLAKE3" in algorithms

    @pytest.mark.parametrize(
        "algorithm",
        [
            "MD5",
            "SHA1",
            "SHA224",
            "SHA256",
            "SHA384",
            "SHA512",
            "SHA3_224",
            "SHA3_256",
            "SHA3_384",
            "SHA3_512",
            "BLAKE2S",
            "BLAKE2B",
            "BLAKE3",
        ],
    )
    def test_hash_text_all_algorithms(self, service, sample_text, algorithm):
        """Test hashing text with all available algorithms."""
        hash_result = service.hash_text(sample_text, algorithm)
        assert isinstance(hash_result, str)
        assert len(hash_result) > 0
        # Hash should be hex string
        assert all(c in "0123456789abcdef" for c in hash_result.lower())

    @pytest.mark.parametrize("algorithm", ["MD5", "SHA1", "SHA256", "BLAKE3"])
    def test_hash_file_common_algorithms(self, service, sample_file, algorithm):
        """Test hashing files with common algorithms."""
        hash_result = service.hash_file(str(sample_file), algorithm)
        assert isinstance(hash_result, str)
        assert len(hash_result) > 0
        assert all(c in "0123456789abcdef" for c in hash_result.lower())

    def test_hash_text_consistency(self, service, sample_text):
        """Test that hashing same text produces same hash."""
        hash1 = service.hash_text(sample_text, "SHA256")
        hash2 = service.hash_text(sample_text, "SHA256")
        assert hash1 == hash2

    def test_hash_file_consistency(self, service, sample_file):
        """Test that hashing same file produces same hash."""
        hash1 = service.hash_file(str(sample_file), "SHA256")
        hash2 = service.hash_file(str(sample_file), "SHA256")
        assert hash1 == hash2

    def test_hash_text_different_algorithms_produce_different_hashes(
        self, service, sample_text
    ):
        """Test that different algorithms produce different hashes."""
        hash_sha256 = service.hash_text(sample_text, "SHA256")
        hash_md5 = service.hash_text(sample_text, "MD5")
        assert hash_sha256 != hash_md5

    def test_hash_text_invalid_algorithm(self, service, sample_text):
        """Test hashing with invalid algorithm raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported algorithm"):
            service.hash_text(sample_text, "INVALID_ALGO")

    def test_hash_file_invalid_algorithm(self, service, sample_file):
        """Test file hashing with invalid algorithm raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported algorithm"):
            service.hash_file(str(sample_file), "INVALID_ALGO")

    def test_hash_file_not_found(self, service):
        """Test hashing non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            service.hash_file("/nonexistent/file.txt", "SHA256")

    def test_hash_empty_text(self, service):
        """Test hashing empty text."""
        hash_result = service.hash_text("", "SHA256")
        assert isinstance(hash_result, str)
        assert len(hash_result) > 0

    def test_known_sha256_hash(self, service):
        """Test against known SHA256 hash."""
        text = "hello"
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        result = service.hash_text(text, "SHA256")
        assert result == expected
