import os

from cryptography.fernet import Fernet
from PyInquirer import Separator, prompt
from termcolor import colored
from stegano import lsb 

from key_gen import key_gen

# Defining the decryption function


def decrypt_func() -> None:
    # Asking the user for a prompt
    enc_info = prompt([
        {
            'type': 'list',
            'qmark': '>',
            'name': 'type_of_data',
            'message': 'What do you want to decrypt?',
            'choices': [
                Separator(),
                {
                    'name': 'Text',
                },
                {
                    'name': 'File',
                },
                {
                    'name': 'Image',
                },
            ],
        },


    ])

    # Storing the type of data in a variable
    type_of_data: str = enc_info['type_of_data']

    # Calling the appropriate function as per data
    if type_of_data == 'File':
        handle_file_dec()
    elif type_of_data == 'Image':
        handle_image_dec()
    else:
        handle_text_dec()


def handle_text_dec() -> None:
    # Using decryption information
    decrypt_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'data',
            'message': 'Enter the text to decrypt.',
        },
        {
            'type': 'password',
            'qmark': '>',
            'name': 'password',
            'message': 'Enter password:',
        },
    ])

    # Storing data in variables
    data: str = decrypt_info['data']
    passW: str = decrypt_info['password']

    # Making sure that the password is not empty
    if not passW:
        print(colored('Please enter a password', 'red'))
        return None

    # Key Generation
    key = key_gen(passW)

    try:
        # Generating cipher
        cipher = Fernet(key)
    except Exception:
        # Handling exceptions
        print(colored('Key Error!', 'red'))
        return None

    try:
        # Trying to decrypt text
        decrypted_text = cipher.decrypt(data.encode()).decode()
    except Exception:
        # Handling wrong key or data
        print(colored('Either the key or the input data is wrong.', 'red'))
        return None

    # Printing the text on the console
    print(colored('The decrypted text is: ', 'white') +
          colored(decrypted_text, 'green'))


def handle_file_dec() -> None:
    # Getting the file info
    file_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'file_name',
            'message': 'Enter the path to the file.',
        },
        {
            'type': 'password',
            'qmark': '>',
            'name': 'password',
            'message': 'Enter the password: ',
        },
    ])

    # Storing the password in a variable
    passW: str = file_info['password']

    # Making sure that the password is not empty
    if not passW:
        print(colored('Please enter a password', 'red'))
        return None

    # Key Generation
    key = key_gen(passW)

    try:
        # Generating cipher
        cipher = Fernet(key)
    except Exception:
        # Handling exceptions
        print(colored('Key Error!', 'red'))
        return None

    try:
        # Getting the size of the file
        file_name: str = file_info['file_name']
        file_size = os.path.getsize(file_name)

        # Making sure that the file size is below 1 GB
        if file_size > 1073741824:
            print(colored("File too large. Only files up to 1GB are supported.", "red"))
            return None

        # Making sure that the file is encrypted
        if 'encrypto' not in file_name:
            print(colored("File is not encrypted.", "yellow"))
            return None

        try:
            # Reading the file as binary
            with open(file_name, 'rb') as file_path:
                encrypted_data = cipher.decrypt(file_path.read())

            # Recreating the original file extension and writing to it
            with open(file_name.replace('encrypto', ''), 'wb') as write_file:
                write_file.write(encrypted_data)
                print(colored('File decrypted successfully.', 'green'))

        except Exception:
            # Handling exceptions
            print(colored("Ran into an issue.", "red"))
            return None

    except Exception:
        # Handling file not found or similar exceptions
        print(colored('Sorry! Can\'t get to the file or ran into an error.', 'red'))


def handle_image_dec():
    # Using decryption information
    decrypt_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'image_path',
            'message': 'Enter the path of the image to decrypt.',
        },
        {
            'type': 'password',
            'qmark': '>',
            'name': 'password',
            'message': 'Enter password:',
        },
    ])

    # Storing data in variables
    passW = decrypt_info['password']

    # Making sure that the password is not empty
    if passW == '':
        print(colored('Please enter a password', 'red'))
        return None

    # Key Generation
    key = key_gen(passW)

    try:
        # Generating cipher
        cipher = Fernet(key)
    except Exception as e:
        # Handling exceptions
        print(colored('Key Error!', 'red'))
        return None

    try:
        # Trying to decrypt text
        data = lsb.reveal(decrypt_info['image_path'])
        decrypted_text = cipher.decrypt(data.encode()).decode()
    
    except Exception as e:
        # Handling wrong key or data
        print(colored('Either the key or the input data is wrong.', 'red'))
        return None

    # Printing the text on the console
    print(colored('The decrypted text is: ', 'white') +
          colored(decrypted_text, 'green'))
