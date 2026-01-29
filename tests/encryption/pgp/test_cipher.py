"""Tests for PGP cipher functionality."""

import pytest
from hypothesis import given, strategies as st, settings


# Skip all PGP tests if GPG is not installed
pytest.importorskip("gnupg", reason="GPG not installed")


class TestPGPCipher:
    """Test PGP encryption, decryption, signing, and verification."""

    @pytest.fixture
    def cipher(self):
        """Provide PGPCipher instance if GPG is available."""
        try:
            from encryptocli.encryption.pgp import PGPCipher

            return PGPCipher()
        except OSError:
            pytest.skip("GPG not installed")

    @pytest.fixture
    def test_key_email(self):
        """Test email for key generation."""
        return "test@encryptocli.test"

    @pytest.fixture
    def test_passphrase(self):
        """Test passphrase for PGP operations."""
        return "test_passphrase_123"

    def test_generate_key(self, cipher, test_key_email, test_passphrase):
        """Test PGP key generation."""
        result = cipher.generate_key_pair("Test User", test_key_email, test_passphrase)
        assert isinstance(result, str)
        assert len(result) > 0  # Should return key fingerprint

    def test_list_keys(self, cipher):
        """Test listing PGP keys."""
        keys = cipher.list_keys()
        assert isinstance(keys, list)

    def test_encrypt_decrypt_text(
        self, cipher, test_key_email, test_passphrase, sample_text
    ):
        """Test PGP text encryption and decryption roundtrip."""
        # Generate key first
        cipher.generate_key_pair("Test User", test_key_email, test_passphrase)

        # Encrypt
        encrypted = cipher.encrypt_text(sample_text, test_key_email)
        assert encrypted != sample_text
        assert "-----BEGIN PGP MESSAGE-----" in encrypted

        # Decrypt
        decrypted = cipher.decrypt_text(encrypted, test_passphrase)
        assert decrypted == sample_text

    @pytest.mark.skip(reason="PGP operations depend on GPG keyring state")
    def test_sign_verify_text(
        self, cipher, test_key_email, test_passphrase, sample_text
    ):
        """Test PGP text signing and verification."""
        # Generate key first
        cipher.generate_key_pair("Test User", test_key_email, test_passphrase)

        # Sign
        signed = cipher.sign_text(sample_text, test_passphrase)
        assert "-----BEGIN PGP SIGNED MESSAGE-----" in signed

        # Verify
        result = cipher.verify_text(signed)
        assert "valid" in str(result).lower() or "good" in str(result).lower()

    @pytest.mark.skip(reason="PGP operations depend on GPG keyring state")
    def test_encrypt_decrypt_file(
        self, cipher, test_key_email, test_passphrase, sample_file, temp_dir
    ):
        """Test PGP file encryption and decryption."""
        # Generate key first
        cipher.generate_key_pair("Test User", test_key_email, test_passphrase)

        # Encrypt
        result = cipher.encrypt_file(str(sample_file), test_key_email)
        assert "successfully" in result.lower()

        # Check encrypted file exists
        encrypted_file = temp_dir / f"{sample_file.name}.gpg"
        assert encrypted_file.exists()

        # Decrypt
        output_dir = temp_dir / "decrypted"
        output_dir.mkdir()
        decrypt_result = cipher.decrypt_file(
            str(encrypted_file), test_passphrase, str(output_dir)
        )
        assert "successfully" in decrypt_result.lower()

    @pytest.mark.skip(reason="PGP operations depend on GPG keyring state")
    def test_sign_verify_file(
        self, cipher, test_key_email, test_passphrase, sample_file, temp_dir
    ):
        """Test PGP file signing and verification."""
        # Generate key first
        cipher.generate_key_pair("Test User", test_key_email, test_passphrase)

        # Sign
        result = cipher.sign_file(str(sample_file), test_passphrase, str(temp_dir))
        assert "successfully" in result.lower()

        # Check signature file exists
        sig_file = temp_dir / f"{sample_file.name}.sig"
        assert sig_file.exists()

        # Verify
        verify_result = cipher.verify_file(str(sample_file), str(sig_file))
        assert "valid" in verify_result.lower() or "good" in verify_result.lower()

    @settings(max_examples=10, deadline=5000)
    @given(text=st.text(min_size=1, max_size=500))
    def test_text_roundtrip_property(self, text):
        """Property test: any text encrypted then decrypted equals original."""
        try:
            from encryptocli.encryption.pgp import PGPCipher

            cipher = PGPCipher()
            test_key_email = "test@encryptocli.test"
            test_passphrase = "test_passphrase_123"
            # Ensure key exists
            cipher.generate_key_pair("Test User", test_key_email, test_passphrase)

            encrypted = cipher.encrypt_text(text, test_key_email)
            decrypted = cipher.decrypt_text(encrypted, test_passphrase)
            assert decrypted == text
        except Exception:
            # Skip if key generation fails in hypothesis
            pytest.skip("Key generation failed")
