"""Tests for encryption service."""

import pytest
from hypothesis import given, strategies as st

from encryptocli.services.encryption_service import EncryptionService


class TestEncryptionService:
    """Test encryption service business logic."""

    @pytest.fixture
    def service(self):
        """Provide EncryptionService instance."""
        return EncryptionService()

    def test_encrypt_text_aes(self, service, sample_text, sample_password):
        """Test AES text encryption through service."""
        encrypted = service.encrypt_text(sample_text, sample_password, method="aes")
        assert encrypted != sample_text
        assert isinstance(encrypted, str)

    def test_encrypt_file_aes(self, service, sample_file, sample_password, temp_dir):
        """Test AES file encryption through service."""
        result = service.encrypt_file(str(sample_file), sample_password, method="aes")
        assert "successfully" in result.lower()
        encrypted_file = temp_dir / f"{sample_file.name}.encrypto"
        assert encrypted_file.exists()

    def test_encrypt_text_default_method(self, service, sample_text, sample_password):
        """Test that default encryption method is AES."""
        encrypted = service.encrypt_text(sample_text, sample_password)
        assert encrypted != sample_text

    @given(text=st.text(min_size=1, max_size=500))
    def test_encrypt_text_any_input(self, text):
        """Property test: service can encrypt any text."""
        service = EncryptionService()
        password = "test_password_123"
        encrypted = service.encrypt_text(text, password)
        assert isinstance(encrypted, str)
        assert len(encrypted) > 0
