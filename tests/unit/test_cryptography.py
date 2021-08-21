import unittest

# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_salt():
    salt = os.urandom(16)
    salt_bytes = base64.b64encode(salt)
    print(salt_bytes)


def get_id(
    plain_text,
    salt_bytes = base64.b64decode("PM4L5YB9bO44vbZoCK7sFw=="), 
    kdf_algorithm=hashes.SHA256(), 
    kdf_length=12, 
    kdf_iteractions=366):
    kdf = PBKDF2HMAC(
        algorithm = kdf_algorithm,
        length = kdf_length,
        salt = salt_bytes,
        iterations = kdf_iteractions
    )
    key = kdf.derive(plain_text.encode('utf-8'))
    print(base64.b64encode(key))
    

def aaaa():
    # salt_b64 = "PM4L5YB9bO44vbZoCK7sFw=="
    # salt_bytes = base64.b64decode(salt_b64)
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(b"my great password")
    
if __name__ == '__main__':
    #unittest.main()
    #generate_salt()
    get_id("my great password")
