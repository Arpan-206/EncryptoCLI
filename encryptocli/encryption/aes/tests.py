import pytest

from encryption.aes import AESCipher
from util.exceptions import FatalError


class TestEncryption:

    @pytest.mark.parametrize("input,password", [("dummytext", "dummypass")])
    def test_basic_encryption_decryption(self, input, password):
        cipher = AESCipher()
        encrypted_text = cipher.encrypt_text(input, password)
        decrypted_text = cipher.decrypt_text(encrypted_text, password)
        assert decrypted_text == input

    @pytest.mark.parametrize("input,password", [("dummytext", "")])
    def test_error_on_no_password(self, input, password):
        cipher = AESCipher()
        with pytest.raises(FatalError):
            cipher.encrypt_text(input, password)

    # def error_on_malformed_key(input, password)
