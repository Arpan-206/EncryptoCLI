import os

from cryptography.fernet import Fernet
from PyInquirer import Separator, prompt
from termcolor import colored
from stegano import lsb

from key_gen import key_gen


# Defining the encryption function
def encrypt_func() -> None:
    # Get user prompt
    enc_info = prompt([
        {
            'type': 'list',
            'qmark': '>',
            'name': 'type_of_data',
            'message': 'What do you want to encrypt?',
            'choices': [
                Separator(),
                {
                    'name': 'Text',
                },
                {
                    'name': 'File',
                },
            ],
        },

    ])


    if 'type_of_data' not in enc_info:
        # user hit Ctrl+C
        return

    # Store the type of data in a variable.
    type_of_data: str = enc_info['type_of_data']

    # Calling the appropriate functions according to the type of the value.
    if type_of_data == 'File':
        handle_file_enc()
    else:
        handle_text_enc()


def handle_text_enc() -> None:
    # Asking the user for data to encrypt
    encrypt_info = prompt([
        {
            'type': 'list',
            'qmark': '>',
            'name': 'type_of_output',
            'message': 'What do you want to encrypt to?',
            'choices': [
                Separator(),
                {
                    'name': 'Image',
                },
                {
                    'name': 'Text',
                },
            ],
        },
        {
            'type': 'input',
            'qmark': '>',
            'name': 'input_image_path',
            'message': 'Enter the path to the image. ( PNG file recommended )',
            'when': lambda answers : answers['type_of_output'] == 'Image',
        },
        {
            'type': 'input',
            'qmark': '>',
            'name': 'data',
            'message': 'Enter the text to encrypt:',
        },
        {
            'type': 'password',
            'qmark': '>',
            'name': 'password',
            'message': 'Enter the password: ',
        },
    ])

    if 'data' not in encrypt_info:
        # user hit Ctrl+C
        return

    # Store the type of output in a variable
    type_of_output = encrypt_info['type_of_output']
    if encrypt_info['type_of_output'] == 'Image':
        input_image_path = encrypt_info['input_image_path']

    # Storing the data into variables
    data: str = encrypt_info['data']
    passW: str = encrypt_info['password']

    # Checking if the user entered a password
    if not passW:
        print(colored('Please enter a password', 'red'))
        return None

    # Key generation
    key = key_gen(passW)


    try:
        # Trying to create a cipher variable as an instance of the Fernet class.
        cipher = Fernet(key)
    except Exception:
        # Handling exceptions
        print(colored('Key Error!', 'red'))
        return None

    # Encrypting the text and storing it in a variable.
    encrypted_text = cipher.encrypt(data.encode()).decode()


    if type_of_output == 'Text':

        # Printing out the data
        print(colored('The encrypted text is: ', 'white') +
            colored(encrypted_text, 'green'))
        return None

    elif type_of_output == 'Image':

        secret = lsb.hide(input_image_path, encrypted_text)
        secret.save("./encrypto.png")


def handle_file_enc() -> None:
    # Asking the user for the file to encrypt
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

    if 'password' not in file_info:
        # user hit Ctrl+C
        return

    # Storing it as a variable
    passW: str = file_info['password']

    # Making sure that the password isn't empty
    if not passW:
        print(colored('Please enter a password', 'red'))
        return None

    # Key generation
    key = key_gen(passW)

    try:
        # Trying to create a cipher variable as an instance of the Fernet class.
        cipher = Fernet(key)
    except Exception:
        # Handling exceptions
        print(colored('Key Error!', 'red'))
        return None

    try:
        # Getting the size of the file
        file_name: str = file_info['file_name']
        file_size = os.path.getsize(file_name)

        # Verifying if the file size is less than 1 GB
        if file_size > 1073741824:
            print(colored("File too large. Only files up to 1GB are supported.", "red"))
            return None

        # Detecting if the file is already encrypted
        if 'encrypto' in file_name:
            print(colored("File is already encrypted.", "yellow"))
            return None

        try:
            # Opening and reading the file as binary
            with open(file_name, 'rb') as file_path:
                encrypted_data = cipher.encrypt(file_path.read())

            # Writing the encrypted data into a new file
            with open(f"{file_name}encrypto", 'wb') as write_file:
                write_file.write(encrypted_data)
                print(colored('File encrypted successfully.', 'green'))

        except Exception:
            # Handling exceptions
            print(colored('Ran into an issue.', 'red'))
            return None

    except Exception:
        # Handling file not found or similar exceptions
        print(colored('Sorry! Can\'t get to the file or ran into an error.', 'red'))
