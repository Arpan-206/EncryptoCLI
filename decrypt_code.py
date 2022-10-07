import os

from cryptography.fernet import Fernet
from PyInquirer import Separator, prompt
from termcolor import colored
from stegano import lsb
from encrypt.aes.decrypt import decrypt_file, decrypt_text 

from util.key_gen import key_gen

# Defining the decryption function


def decrypt_func():
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
    type_of_data = enc_info['type_of_data']

    # Calling the appropriate function as per data
    if type_of_data == 'File':
        handle_file_dec()
    elif type_of_data == 'Image':
        handle_image_dec()
    else:
        handle_text_dec()


def handle_text_dec():
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
    encrypted_secret = decrypt_info['data']
    password = decrypt_info['password']

    decrypted_text = decrypt_text(encrypted_secret, password)

    # Printing the text on the console
    print(colored('The decrypted text is: ', 'white') +
          colored(decrypted_text, 'green'))


def handle_file_dec():
    # Getting the file info
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

    # Storing the password in a variable
    password = file_info['password']
    file_path = file_info['file_path']

    decrypt_file(file_path, password)
    print(colored('File decrypted succesfully.', 'green'))

    # print(colored("Ran into an issue.", "red"))


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
