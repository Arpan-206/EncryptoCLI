# Importing 3rd Party Libraries
from pyfiglet import Figlet
from PyInquirer import prompt, Separator
from termcolor import colored

# Importing the local functions
from encrypt_code import encrypt_func
from decrypt_code import decrypt_func
from hash_code import hash_func

# Generating the initial output text with pyfiglet
f = Figlet(font='slant')
credit = colored('                                                 By Arpan Pandey\n', 'yellow', attrs=['bold'])
description = colored(
    '  A tool to hash or encrypt your data easily using Fernet Encryption. It is very easy and intuitive to use. You can also use this on any type of file below 1GB.', 'cyan')
print(colored(f.renderText('Encrypto CLI'), 'green'), credit, description, '\n')

# Asking the user about which operation do they want to perform
operation = prompt([
    {
        'type': 'list',
        'qmark': '🔘',
        'name': 'operation',
        'message': 'What do you want to do?',
        'choices': [
            Separator(),
            {
                'name': 'Hash',
            },
            {
                'name': 'Encrypt',
            },
            {
                'name': 'Decrypt',
            },
        ],
    }
])['operation']

# Calling the hash function if the selected operation is Hashing
if operation == 'Hash':
    # * Called the hashing function
    hash_func()

# Calling the Encryption function if the selected operation is encryption
elif operation == 'Encrypt':
    # * Called the encryption function
    encrypt_func()

# Calling the decryption function if the selected operation is decryption
else:
    # * Called the decryption function
    decrypt_func()
