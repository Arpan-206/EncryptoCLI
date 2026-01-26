from pathlib import Path
import pytest
import shutil

from steganography.lsb import LSBSteganography


class TestEncryption:
    """
    Tests for the encryption and decryption of text
    """

    @pytest.mark.parametrize("input", ["dummytext"])
    def test_basic_encryption_decryption(self, tmp_path, input):
        path = tmp_path / "stegano_test_data"
        path.mkdir()
        shutil.copy2(Path().absolute().joinpath("test_files/gg.png"), path)
        steg = LSBSteganography()
        steg.encrypt_text(str(path) + "/gg.png", input, str(path.absolute()))
        decrypted_text = steg.decrypt_image(str(path.absolute()) + "encrypto.png")
        assert decrypted_text == input

    # def error_on_malformed_key(input, password)
