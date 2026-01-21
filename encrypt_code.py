
from InquirerPy import inquirer
from termcolor import colored
import encryption.aes
import steganography.lsb


# Defining the encryption function
def encrypt_func() -> None:
    # Get user prompt
    type_of_data = inquirer.select(
        message='What do you want to encrypt?',
        choices=['Text', 'File'],
    ).execute()

    if not type_of_data:
        # user hit Ctrl+C
        return

    # Calling the appropriate functions according to the type of the value.
    if type_of_data == 'File':
        handle_file_enc()
    else:
        handle_text_enc()


def handle_text_enc() -> None:
    # Asking the user for data to encrypt
    type_of_output = inquirer.select(
        message='What do you want to encrypt to?',
        choices=['Image', 'Text'],
    ).execute()
    
    if not type_of_output:
        # user hit Ctrl+C
        return
    
    # Ask for additional inputs based on output type
    input_image_path = None
    if type_of_output == 'Image':
        input_image_path = inquirer.text(
            message='Enter the path to the image. ( PNG file recommended )'
        ).execute()
        if not input_image_path:
            return
    
    secret = inquirer.text(
        message='Enter the text to encrypt:'
    ).execute()
    
    if not secret:
        # user hit Ctrl+C
        return
    
    password = inquirer.secret(
        message='Enter the password: '
    ).execute()
    
    if not password:
        # user hit Ctrl+C
        return

    encrypted_text = encryption.aes.encrypt_text(secret, password)

    if type_of_output == 'Text':
        # Printing out the data
        print(colored('The encrypted text is: ', 'white') +
            colored(encrypted_text, 'green'))
        return None

    elif type_of_output == 'Image':
        steganography.lsb.encrypt_text(input_image_path, encrypted_text, "./")

        

def handle_file_enc() -> None:
    # Asking the user for the file to encrypt
    file_path = inquirer.text(
        message='Enter the path to the file.'
    ).execute()
    
    if not file_path:
        # user hit Ctrl+C
        return
    
    password = inquirer.secret(
        message='Enter the password: '
    ).execute()
    
    if not password:
        # user hit Ctrl+C
        return

    encryption.aes.encrypt.encrypt_file( file_path, password )
