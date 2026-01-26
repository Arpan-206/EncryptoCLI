#### all prompts are kept in one place so that its easier to modify the prompt appearance ####


def text_to_encrypt(
    name="to_encrypt_text", message="Enter the text to encrypt:", when=None
):
    return (
        {"type": "input", "qmark": ">", "name": name, "message": message, "when": when},
    )


def password(name="password"):
    return {
        "type": "password",
        "qmark": ">",
        "name": name,
        "message": "Enter the password: ",
    }


def image_path():
    return (
        {
            "type": "input",
            "qmark": ">",
            "name": "input_image_path",
            "message": "Enter the path to the image. ( PNG file recommended )",
            "when": lambda answers: answers["type_of_output"] == "Image",
        },
    )
