"""Tests for AES cipher functionality."""

import pytest
from hypothesis import given, strategies as st

from encryptocli.encryption.aes import AESCipher
from encryptocli.util.exceptions import FatalError, MildError


class TestAESCipher:
    """Test AES encryption and decryption."""

    @pytest.fixture
    def cipher(self):
        """Provide AESCipher instance."""
        return AESCipher()

    def test_encrypt_text_success(self, cipher, sample_text, sample_password):
        """Test successful text encryption."""
        encrypted = cipher.encrypt_text(sample_text, sample_password)
        assert encrypted != sample_text
        assert isinstance(encrypted, str)
        assert len(encrypted) > 0

    def test_decrypt_text_success(self, cipher, sample_text, sample_password):
        """Test successful text decryption."""
        encrypted = cipher.encrypt_text(sample_text, sample_password)
        decrypted = cipher.decrypt_text(encrypted, sample_password)
        assert decrypted == sample_text

    def test_encrypt_text_empty_password(self, cipher, sample_text):
        """Test encryption with empty password raises error."""
        with pytest.raises(FatalError, match="Please enter a password"):
            cipher.encrypt_text(sample_text, "")

    def test_decrypt_text_empty_password(self, cipher, sample_text):
        """Test decryption with empty password raises error."""
        with pytest.raises(FatalError, match="Please enter a password"):
            cipher.decrypt_text(sample_text, "")

    def test_decrypt_text_wrong_password(self, cipher, sample_text, sample_password):
        """Test decryption with wrong password raises error."""
        encrypted = cipher.encrypt_text(sample_text, sample_password)
        with pytest.raises(
            FatalError, match="Either the key or the input data is wrong"
        ):
            cipher.decrypt_text(encrypted, "wrong_password")

    def test_encrypt_file_success(self, cipher, sample_file, sample_password, temp_dir):
        """Test successful file encryption."""
        result = cipher.encrypt_file(str(sample_file), sample_password)
        assert result == "File encrypted successfully"
        encrypted_file = temp_dir / f"{sample_file.name}.encrypto"
        assert encrypted_file.exists()

    def test_decrypt_file_success(self, cipher, sample_file, sample_password, temp_dir):
        """Test successful file decryption."""
        # First encrypt
        cipher.encrypt_file(str(sample_file), sample_password)
        encrypted_file = temp_dir / f"{sample_file.name}.encrypto"

        # Then decrypt
        cipher.decrypt_file(str(encrypted_file), sample_password)
        decrypted_file = temp_dir / sample_file.name
        assert decrypted_file.exists()
        assert decrypted_file.read_text() == "Sample file content for testing."

    def test_encrypt_file_already_encrypted(
        self, cipher, sample_file, sample_password, temp_dir
    ):
        """Test encrypting already encrypted file raises error."""
        # First encrypt
        cipher.encrypt_file(str(sample_file), sample_password)
        encrypted_file = temp_dir / f"{sample_file.name}.encrypto"

        # Try to encrypt again
        with pytest.raises(MildError, match="File is already encrypted"):
            cipher.encrypt_file(str(encrypted_file), sample_password)

    @given(text=st.text(min_size=1, max_size=1000))
    def test_text_roundtrip_property(self, text):
        """Property test: any text encrypted then decrypted equals original."""
        cipher = AESCipher()
        password = "test_password_123"
        encrypted = cipher.encrypt_text(text, password)
        decrypted = cipher.decrypt_text(encrypted, password)
        assert decrypted == text

    @given(
        text=st.text(min_size=1, max_size=100),
        password=st.text(min_size=1, max_size=50),
    )
    def test_different_passwords_produce_different_ciphertext(self, text, password):
        """Property test: same text with different passwords produces different ciphertext."""
        if len(password) < 2:
            return

        cipher = AESCipher()
        password1 = password
        password2 = password + "x"

        encrypted1 = cipher.encrypt_text(text, password1)
        encrypted2 = cipher.encrypt_text(text, password2)
        assert encrypted1 != encrypted2
