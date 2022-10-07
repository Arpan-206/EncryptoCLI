
from PyInquirer import Separator, prompt
from termcolor import colored
import encryption.aes
import steganography


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
            'name': "secret",
            'message': "Enter the text to encrypt:",
        },
        {
            'type': 'password',
            'qmark': '>',
            'name': 'password',
            'message': 'Enter the password: ',
        },
    ])

    if 'secret' not in encrypt_info:
        # user hit Ctrl+C
        return

    # Store the type of output in a variable
    type_of_output = encrypt_info['type_of_output']
    if encrypt_info['type_of_output'] == 'Image':
        input_image_path = encrypt_info['input_image_path']

    # Storing the data into variables
    secret = encrypt_info['secret']
    password = encrypt_info['password']

    encrypted_text = encryption.aes.encrypt_text(secret, password)

    print(type_of_output)

    if type_of_output == 'Text':

        # Printing out the data
        print(colored('The encrypted text is: ', 'white') +
            colored(encrypted_text, 'green'))
        return None

    elif type_of_output == 'Image':

        encrypted_secret = encryption.aes.encrypt_text(secret, password)
        steganography.lsb.encrypt_text(input_image_path, encrypted_secret)

        

def handle_file_enc() -> None:
    # Asking the user for the file to encrypt
    file_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'file_path',
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
    password = file_info['password']
    file_path = file_info['file_path']

    encryption.aes.encrypt.encrypt_file( file_path, password )
