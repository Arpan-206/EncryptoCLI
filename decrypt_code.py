from base64 import urlsafe_b64encode
from hashlib import scrypt
import random
import os
from cryptography.fernet import Fernet
from PyInquirer import prompt, Separator
from termcolor import colored

def decrypt_func():
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
            ],
        },


    ])

    type_of_data = enc_info['type_of_data']

    if type_of_data == 'File':
        handle_file_dec()
    else:
        handle_text_dec()


def handle_text_dec():
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

    data = decrypt_info['data']
    passW = decrypt_info['password']

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
        decrypted_text = cipher.decrypt(data.encode()).decode()
    except Exception as e:
        print(colored('Either the key or the input data is wrong.', 'red'))
        return None

    print(colored('The decrypted text is: ', 'white') +
          colored(decrypted_text, 'green'))

def handle_file_dec():
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

        if 'encrypto' not in file_info['file_name']:
            print(colored("File is not encrypted.", "yellow"))
            return None

        try:
            with open(file_info['file_name'], 'rb') as file_path:
                encrypted_data = cipher.decrypt(file_path.read())

                with open(f"{file_info['file_name'].replace('encrypto', '')}", "wb") as write_file:
                    write_file.write(encrypted_data)
                    print(colored('File decrypted succesfully.', 'green'))
                    
        except Exception as e:
            print(colored("Ran into an issue.", "red"))
            return None

    except Exception as e:
        print(colored('Sorry! Can\'t get to the file or ran into an error.', 'red'))
