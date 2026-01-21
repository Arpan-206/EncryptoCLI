
import inquirer
from termcolor import colored
import encryption.aes
import steganography.lsb


# Defining the encryption function
def encrypt_func() -> None:
    # Get user prompt
    enc_info = inquirer.prompt([
        inquirer.List(
            'type_of_data',
            message='What do you want to encrypt?',
            choices=['Text', 'File'],
        ),
    ])

    if not enc_info:
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
    encrypt_info = inquirer.prompt([
        inquirer.List(
            'type_of_output',
            message='What do you want to encrypt to?',
            choices=['Image', 'Text'],
        ),
    ])
    
    if not encrypt_info:
        return
    
    type_of_output = encrypt_info['type_of_output']
    
    # Ask for additional inputs based on output type
    additional_questions = []
    if type_of_output == 'Image':
        additional_questions.append(
            inquirer.Text('input_image_path', message='Enter the path to the image. ( PNG file recommended )')
        )
    
    additional_questions.extend([
        inquirer.Text('secret', message='Enter the text to encrypt:'),
        inquirer.Password('password', message='Enter the password: '),
    ])
    
    encrypt_info.update(inquirer.prompt(additional_questions) or {})

    if 'secret' not in encrypt_info:
        # user hit Ctrl+C
        return

    # Storing the data into variables
    secret = encrypt_info['secret']
    password = encrypt_info['password']

    encrypted_text = encryption.aes.encrypt_text(secret, password)

    if type_of_output == 'Text':

        # Printing out the data
        print(colored('The encrypted text is: ', 'white') +
            colored(encrypted_text, 'green'))
        return None

    elif type_of_output == 'Image':
        print(input_image_path)
        steganography.lsb.encrypt_text(input_image_path, encrypted_text, "./")

        

def handle_file_enc() -> None:
    # Asking the user for the file to encrypt
    file_info = inquirer.prompt([
        inquirer.Text('file_path', message='Enter the path to the file.'),
        inquirer.Password('password', message='Enter the password: '),
    ])

    if not file_info or 'password' not in file_info:
        # user hit Ctrl+C
        return

    # Storing it as a variable
    password = file_info['password']
    file_path = file_info['file_path']

    encryption.aes.encrypt.encrypt_file( file_path, password )
