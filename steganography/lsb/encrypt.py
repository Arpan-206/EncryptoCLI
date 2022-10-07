from stegano import lsb


def encrypt_text(input_image_path, secret):
    secret = lsb.hide(input_image_path, secret)
    secret.save("./encrypto.png")

