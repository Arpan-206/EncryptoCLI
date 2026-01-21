
from stegano import lsb

def decrypt_image(input_image_path):
    """
    Decrypts the image
    """
    decrypted_text = lsb.reveal(input_image_path)

    return decrypted_text
