
from cryptography.fernet import Fernet
from termcolor import colored
from util.exceptions import FatalError
from util.file_handling import get_file
from util.key_gen import key_gen


def decrypt_text(encrypted_secret, password):

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
        raise FatalError("Key Exception!")


    try:
        # Trying to decrypt text
        decrypted_text = cipher.decrypt(encrypted_secret.encode()).decode()
    except Exception as e:
        # Handling wrong key or data
        raise FatalError("Either the key or the input data is wrong.")


    return decrypted_text


def decrypt_file(file_path, password):
    # Making sure that the password is not empty
    if password == '':
        raise FatalError('Please enter a password')

    # Key Generation
    key = key_gen(password)

    try:
        # Generating cipher
        cipher = Fernet(key)
    except Exception as e:
        # Handling exceptions
        print(colored('Key Error!', 'red'))
        return None

        
    file = get_file(file_path)


    try:
        # Reading the file as binary and encrypting
        encrypted_data = cipher.decrypt(file.read())

    except:
        raise FatalError("Ran into an issue while encrypting file")


    try:
        # Recreating the original file with extension and writing to it
        with open(f"{file.name.replace('.encrypto', '')}", "wb") as write_file:
            write_file.write(encrypted_data)
                
    except Exception as e:
        # Handling exceptions
        raise FatalError("Ran into an issue while writing to file")

