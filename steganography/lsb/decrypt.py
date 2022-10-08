
from cryptography.fernet import Fernet
from util.exceptions import FatalError
from util.key_gen import key_gen

from stegano import lsb

def decrypt_image(input_image_path):

    decrypted_text = lsb.reveal(input_image_path)

    return decrypted_text
