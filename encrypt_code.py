from base64 import urlsafe_b64encode
from hashlib import scrypt
import random
import os

from cryptography.fernet import Fernet
from PyInquirer import prompt, Separator
from termcolor import colored


def encrypt_func():
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

    type_of_data = enc_info['type_of_data']

    if type_of_data == 'File':
        handle_file_enc()
    else:
        handle_text_enc()


def handle_text_enc():
    encrypt_info = prompt([
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

    data = encrypt_info['data']
    passW = encrypt_info['password']

    if passW == '':
        print(colored('Please enter a password', 'red'))
        return None

    random.seed(passW)
    salt = f"{ random.random() }".encode()
    key = urlsafe_b64encode(
        scrypt(passW.encode(), salt=salt, n=16384, r=8, p=1, dklen=32))

    try:
        cipher = Fernet(key)
    except Exception as e:
        print(colored('Key Error!', 'red'))
        return None
    encrypted_text = cipher.encrypt(data.encode()).decode()

    print(colored('The encrypted text is: ', 'white') +
          colored(encrypted_text, 'green'))


def handle_file_enc():
    file_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'file_name',
            'message': 'Enter the name of the file.',
        },
        {
            'type': 'password',
            'qmark': '>',
            'name': 'password',
            'message': 'Enter the password: ',
        },
    ])

    passW = file_info['password']

    if passW == '':
        print(colored('Please enter a password', 'red'))
        return None

    random.seed(passW)
    salt = f"{ random.random() }".encode()
    key = urlsafe_b64encode(
        scrypt(passW.encode(), salt=salt, n=16384, r=8, p=1, dklen=32))

    try:
        cipher = Fernet(key)
    except Exception as e:
        print(colored('Key Error!', 'red'))
        return None

    try:
        file_size = os.path.getsize(f'{file_info["file_name"]}')

        if file_size > 1073741824:
            print(colored("File too large. Only files till 1GB are supported.", "red"))
            return None

        if 'encrypto' in file_info['file_name']:
            print(colored("File is already encrypted.", "yellow"))
            return None

        try:
            with open(file_info['file_name'], 'rb') as file_path:
                encrypted_data = cipher.encrypt(file_path.read())

                with open(f"{file_info['file_name']}encrypto", "wb") as write_file:
                    write_file.write(encrypted_data)
                    print(colored('File encrypted succesfully.', 'green'))
                    
        except Exception as e:
            print(colored("Ran into an issue.", "red"))
            return None

    except Exception as e:
        print(colored('Sorry! Can\'t get to the file or ran into an error.', 'red'))
