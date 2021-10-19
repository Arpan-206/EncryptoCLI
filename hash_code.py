import hashlib

from PyInquirer import Separator, prompt
from termcolor import colored


def hash_func():
    hash_info = prompt([
        {
            'type': 'list',
            'qmark': '>',
            'name': 'algorithm',
            'message': 'Which algorithm do you want to use?',
            'choices': [
                Separator(),
                {
                    'name': 'MD5',
                },
                {
                    'name': 'SHA256',
                },
                {
                    'name': 'SHA512',
                },
                {
                    'name': 'BLAKE2',
                },
                {
                    'name': 'BLAKE2b',
                },
            ],
        },
        {
            'type': 'list',
            'qmark': '>',
            'name': 'type_of_data',
            'message': 'What do you want to hash?',
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

    algorithm = hash_info['algorithm']
    type_of_data = hash_info['type_of_data']

    if type_of_data == 'File':
        handle_file_hashing(algorithm)
    else:
        handle_text_hashing(algorithm)


def handle_text_hashing(algorithm):
    data_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'hash_data',
            'message': 'Enter data to hash.',
        },
    ])

    if algorithm == 'MD5':
        hash_out = hashlib.md5()
    elif algorithm == 'SHA256':
        hash_out = hashlib.sha256()
    elif algorithm == 'SHA512':
        hash_out = hashlib.sha512()
    elif algorithm == 'BLAKE2':
        hash_out = hashlib.blake2s()
    else:
        hash_out = hashlib.blake2b()

    hash_out.update(data_info['hash_data'].encode())

    hash_out = hash_out.hexdigest()

    print(colored('Your hash is: ', 'white') + colored(hash_out, 'green'))


def handle_file_hashing(algorithm):
    file_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'file_name',
            'message': 'Enter the name of the file.',
        },
    ])

    try:
        if algorithm == 'MD5':
            hash_out = hashlib.md5()
        elif algorithm == 'SHA256':
            hash_out = hashlib.sha256()
        elif algorithm == 'SHA512':
            hash_out = hashlib.sha512()
        elif algorithm == 'BLAKE2':
            hash_out = hashlib.blake2s()
        else:
            hash_out = hashlib.blake2b()

        with open(file_info['file_name'], 'rb') as file_path:

            chunk = 0
            while chunk != b'':
                chunk = file_path.read(1024)
                hash_out.update(chunk)

        hash_out = hash_out.hexdigest()

        print(colored('Your hash is: ', 'white') + colored(hash_out, 'green'))

    except Exception as e:
        print(colored(
            'Can\'t find the file please check the name and make sure the extension is also present.', 'red'))
