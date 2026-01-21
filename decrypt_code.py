from InquirerPy import inquirer
from termcolor import colored
import encryption.aes
import steganography.lsb

# Defining the decryption function


def decrypt_func() -> None:
    # Asking the user for a prompt
    type_of_data = inquirer.select(
        message='What do you want to decrypt?',
        choices=['Text', 'File', 'Image'],
    ).execute()
    
    if not type_of_data:
        # user hit Ctrl+C
        return

    # Calling the appropriate function as per data
    if type_of_data == 'File':
        handle_file_dec()
    elif type_of_data == 'Image':
        handle_image_dec()
    else:
        handle_text_dec()


def handle_text_dec() -> None:
    # Using decryption information
    data = inquirer.text(
        message='Enter the text to decrypt'
    ).execute()
    
    if not data:
        # user hit Ctrl+C
        return
    
    password = inquirer.secret(
        message='Enter password'
    ).execute()
    
    if not password:
        # user hit Ctrl+C
        return

    # Storing data in variables
    encrypted_secret = data

    decrypted_text = encryption.aes.decrypt_text(encrypted_secret, password)

    # Printing the text on the console
    print(colored('The decrypted text is: ', 'white') +
          colored(decrypted_text, 'green'))


def handle_file_dec() -> None:
    # Getting the file info
    file_path = inquirer.text(
        message='Enter the path to the file'
    ).execute()
    
    if not file_path:
        # user hit Ctrl+C
        return
    
    password = inquirer.secret(
        message='Enter the password'
    ).execute()
    
    if not password:
        # user hit Ctrl+C
        return

    encryption.aes.decrypt_file(file_path, password)
    print(colored('File decrypted succesfully.', 'green'))

    # print(colored("Ran into an issue.", "red"))


def handle_image_dec():
    # Using decryption information
    image_path = inquirer.text(
        message='Enter the path of the image to decrypt'
    ).execute()
    
    if not image_path:
        return
    
    password = inquirer.secret(
        message='Enter password'
    ).execute()
    
    if not password:
        return


    # Trying to decrypt text
    data = steganography.lsb.decrypt_image(image_path)
    decrypted_text = encryption.aes.decrypt_text(data, password)


    # Printing the text on the console
    print(colored('The decrypted text is: ', 'white') +
          colored(decrypted_text, 'green'))

