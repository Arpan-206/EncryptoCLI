import pytest

from encryption.aes.encrypt import encrypt_text, encrypt_file
from encryption.aes.decrypt import decrypt_text, decrypt_file
from util.exceptions import FatalError


class TestEncryption:


    @pytest.mark.parametrize(
        "input,password", 
        [("dummytext","dummypass")]
    )
    def test_basic_encryption_decryption(self, input, password):
        encrypted_text = encrypt_text(input, password)
        decrypted_text = decrypt_text(encrypted_text, password)
        assert decrypted_text == input



    @pytest.mark.parametrize(
        "input,password", 
        [("dummytext","")]
    )
    def test_error_on_no_password(self, input, password):
        with pytest.raises(FatalError):
            encrypt_text(input, password)
            

    # def error_on_malformed_key(input, password)