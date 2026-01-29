"""Tests for decryption service."""

import pytest
from hypothesis import given, strategies as st

from encryptocli.services.decryption_service import DecryptionService
from encryptocli.services.encryption_service import EncryptionService


class TestDecryptionService:
    """Test decryption service business logic."""

    @pytest.fixture
    def service(self):
        """Provide DecryptionService instance."""
        return DecryptionService()

    @pytest.fixture
    def enc_service(self):
        """Provide EncryptionService instance for setup."""
        return EncryptionService()

    def test_decrypt_text_aes(self, service, enc_service, sample_text, sample_password):
        """Test AES text decryption through service."""
        encrypted = enc_service.encrypt_text(sample_text, sample_password, method="aes")
        decrypted = service.decrypt_text(encrypted, sample_password, method="aes")
        assert decrypted == sample_text

    def test_decrypt_file_aes(
        self, service, enc_service, sample_file, sample_password, temp_dir
    ):
        """Test AES file decryption through service."""
        # Encrypt first
        enc_service.encrypt_file(str(sample_file), sample_password, method="aes")
        encrypted_file = temp_dir / f"{sample_file.name}.encrypto"

        # Decrypt
        result = service.decrypt_file(
            str(encrypted_file), sample_password, method="aes"
        )
        assert "successfully" in result.lower()
        decrypted_file = temp_dir / sample_file.name
        assert decrypted_file.exists()

    def test_decrypt_text_default_method(
        self, service, enc_service, sample_text, sample_password
    ):
        """Test that default decryption method is AES."""
        encrypted = enc_service.encrypt_text(sample_text, sample_password)
        decrypted = service.decrypt_text(encrypted, sample_password)
        assert decrypted == sample_text

    @given(text=st.text(min_size=1, max_size=500))
    def test_roundtrip_any_text(self, text):
        """Property test: encrypt then decrypt returns original for any text."""
        enc_service = EncryptionService()
        service = DecryptionService()
        password = "test_password_123"
        encrypted = enc_service.encrypt_text(text, password)
        decrypted = service.decrypt_text(encrypted, password)
        assert decrypted == text
