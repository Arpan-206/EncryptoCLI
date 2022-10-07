from cryptography.fernet import Fernet
from termcolor import colored
from util.exceptions import FatalError
from util.file_handling import get_file

from util.key_gen import key_gen
import util.prompts as prompts
import os


def encrypt_text(secret, password):

    # Storing the data into variables
    if password == '':
        raise FatalError("Please enter a password")


    # Key generation
    key = key_gen(password)


    try:
        # Trying to create a cipher variable as an instance of the Fernet class.
        cipher = Fernet(key)
    except Exception as e:
        raise FatalError('Key Error!')
    

    encrypted_text = cipher.encrypt(secret.encode()).decode()


    return encrypted_text



def encrypt_file(file_path, password):

    # Making sure that the password isn't empty
    if password == '':
        raise FatalError("Please enter a password")

    # Key generation
    key = key_gen(password)

    try:
        # Trying to create a cipher variable as an instance of the Fernet class.
        cipher = Fernet(key)
    except Exception as e:
        raise FatalError('Key Error!')

    # opening the file
    file = get_file(file_path)


    try:
        #reading the file as binary
        encrypted_data = cipher.encrypt(file.read())
    except:
        raise FatalError("Ran into an issue while encrypting file")


    try:
        # Writing the encrypted data into a new file
        with open(f"{file.name}.encrypto", "wb") as write_file:
            write_file.write(encrypted_data)
            print(colored('File encrypted succesfully.', 'green'))
    except:
        raise FatalError("Error while writing to file")




