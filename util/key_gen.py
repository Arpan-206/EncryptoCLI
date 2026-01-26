import random
from base64 import urlsafe_b64encode
from hashlib import scrypt


# Generate key for Fernet encryption
def key_gen(passW: str) -> bytes:
    # Using the password itself as a seed to random to keep salt for scrypt consistent across devices and platforms
    random.seed(passW)
    salt = f"{ random.random() }".encode()
    key = urlsafe_b64encode(
        scrypt(passW.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    )

    return key
