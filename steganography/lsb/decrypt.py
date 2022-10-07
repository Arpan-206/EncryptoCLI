
from cryptography.fernet import Fernet
from util.exceptions import FatalError
from util.key_gen import key_gen

from stegano import lsb

def decrypt_image(input_image_path, password):

    # Making sure that the password is not empty
    if password == '':
        raise FatalError("Please enter a password")

    # Key Generation
    key = key_gen(password)


    try:
        # Generating cipher
        cipher = Fernet(key)
    except Exception as e:
        # Handling exceptions
        raise FatalError("Key Error!")


    try:
        # Trying to decrypt text
        data = lsb.reveal(input_image_path)
        decrypted_text = cipher.decrypt(data.encode()).decode()
    
    except Exception as e:
        # Handling wrong key or data
        raise FatalError("Either the key or the input data is wrong.")


    return decrypted_text
