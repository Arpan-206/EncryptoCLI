# Importing the hashing library
import hashlib

# Importing the visual libraries
from PyInquirer import Separator, prompt
from termcolor import colored

# Defining the hash function.


def hash_func() -> None:
    # Asking the user for further data regarding algorithms
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

    # Storing the data into separate variables
    algorithm: str = hash_info['algorithm']
    type_of_data: str = hash_info['type_of_data']

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

    # Determining the type of data to hash and calling the appropriate functions
    if type_of_data == 'File':
        handle_file_hashing(hash_out)
    else:
        handle_text_hashing(hash_out)


def handle_text_hashing(hash_out) -> None:
    # Asking the user for the data
    data_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'hash_data',
            'message': 'Enter data to hash.',
        },
    ])

    # Populating it the data after converting it to binary
    hash_out.update(data_info['hash_data'].encode())

    # Calculating the actual hash
    final_data = hash_out.hexdigest()

    # Printing out the hash
    print(colored('Your hash is: ', 'white') + colored(final_data, 'green'))
    return None


def handle_file_hashing(hash_out) -> None:
    # Asking the user for the path to the file
    file_info = prompt([
        {
            'type': 'input',
            'qmark': '>',
            'name': 'file_name',
            'message': 'Enter the path to the file.',
        },
    ])

    file_name: str = file_info['file_name']

    try:
        # Again, Defining the hash_out variable according to the algorithm selected by user
        

        # Populating it the data after converting it to binary but this time in chunks so as to not put too much strain on memory
        with open(file_name, 'rb') as file_path:
            chunk = 0
            while chunk != b'':
                chunk = file_path.read(1024)
                hash_out.update(chunk)

        # Calculating the actual hash
        final_hash = hash_out.hexdigest()

        # Printing out the hash
        print(colored('Your hash is: ', 'white') + colored(final_hash, 'green'))

    except Exception:
        print(colored(
            'Can\'t find the file please check the name and make sure the extension is also present.', 'red'))
