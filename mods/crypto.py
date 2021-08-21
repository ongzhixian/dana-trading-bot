import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_salt(bytes_length=16, as_bytes=False):
    salt_bytes = os.urandom(bytes_length)
    if as_bytes:
        return salt_bytes
    return base64.b64encode(salt_bytes)

def get_id(
    plain_text,
    salt_bytes = base64.b64decode("PM4L5YB9bO44vbZoCK7sFw=="), 
    kdf_algorithm=hashes.SHA256(), 
    kdf_length=12, 
    kdf_iteractions=366,
    as_bytes=False
    ):
    kdf = PBKDF2HMAC(
        algorithm = kdf_algorithm,
        length = kdf_length,
        salt = salt_bytes,
        iterations = kdf_iteractions
    )
    key_bytes = kdf.derive(plain_text.encode('utf-8'))
    if as_bytes:
        return key_bytes
    return base64.b64encode(key_bytes)
