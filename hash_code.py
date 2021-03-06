# Importing the hashing library
import hashlib

# Importing the visual libraries
from PyInquirer import Separator, prompt
from termcolor import colored

# Defining the hash function.


def hash_func():
    # Asking the user for further data regarding algoritms
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

    # Storing the data into seperate variables
    algorithm = hash_info['algorithm']
    type_of_data = hash_info['type_of_data']

    # Determining the type of data to hash and calling the appropriate functions
    if type_of_data == 'File':
        handle_file_hashing(algorithm)
    else:
        handle_text_hashing(algorithm)


def handle_text_hashing(algorithm):
    # Asking the user for the data
    data_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'hash_data',
            'message': 'Enter data to hash.',
        },
    ])

    # Defining the hash_out variable according to the algorithm selected by user
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

    # Populating it the data after converting it to binary
    hash_out.update(data_info['hash_data'].encode())

    # Calculating the actual hash
    hash_out = hash_out.hexdigest()

    # Printing out the hash
    print(colored('Your hash is: ', 'white') + colored(hash_out, 'green'))
    return None


def handle_file_hashing(algorithm):
    # Asking the user for the path to the file
    file_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'file_name',
            'message': 'Enter the path to the file.',
        },
    ])

    try:
        # Again, Defining the hash_out variable according to the algorithm selected by user

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

        # Populating it the data after converting it to binary but this time in chunks so as to not put too much strain on memory
        with open(file_info['file_name'], 'rb') as file_path:

            chunk = 0
            while chunk != b'':
                chunk = file_path.read(1024)
                hash_out.update(chunk)

        # Calculating the actual hash
        hash_out = hash_out.hexdigest()

        # Printing out the hash
        print(colored('Your hash is: ', 'white') + colored(hash_out, 'green'))

    except Exception as e:
        print(colored(
            'Can\'t find the file please check the name and make sure the extension is also present.', 'red'))
