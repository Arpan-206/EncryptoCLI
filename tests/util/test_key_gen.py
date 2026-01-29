"""Tests for key generation utility."""

import pytest
from hypothesis import given, strategies as st

from encryptocli.util.key_gen import key_gen


class TestKeyGeneration:
    """Test cryptographic key generation."""

    def test_key_gen_returns_bytes(self, sample_password):
        """Test that key_gen returns bytes."""
        key = key_gen(sample_password)
        assert isinstance(key, bytes)

    def test_key_gen_deterministic(self, sample_password):
        """Test that same password generates same key."""
        key1 = key_gen(sample_password)
        key2 = key_gen(sample_password)
        assert key1 == key2

    def test_key_gen_different_passwords_different_keys(self):
        """Test that different passwords generate different keys."""
        key1 = key_gen("password1")
        key2 = key_gen("password2")
        assert key1 != key2

    def test_key_gen_valid_length(self, sample_password):
        """Test that generated key has valid length for Fernet."""
        key = key_gen(sample_password)
        # Fernet keys are 44 bytes when base64 encoded
        assert len(key) == 44

    @given(password=st.text(min_size=1, max_size=100))
    def test_key_gen_deterministic_property(self, password):
        """Property test: same password always generates same key."""
        key1 = key_gen(password)
        key2 = key_gen(password)
        assert key1 == key2

    @given(password=st.text(min_size=1, max_size=100))
    def test_key_gen_valid_format_property(self, password):
        """Property test: all generated keys are valid Fernet keys."""
        key = key_gen(password)
        assert isinstance(key, bytes)
        assert len(key) == 44
        # Should be base64url encoded
        try:
            key.decode("ascii")
        except UnicodeDecodeError:
            pytest.fail("Key is not valid ASCII/base64")
