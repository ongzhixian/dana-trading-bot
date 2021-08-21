import unittest
from mods.crypto import generate_salt, get_id

class TestCrypto(unittest.TestCase):

    # generate_salt

    def test_generate_salt_16_base64(self):
        # When I generate a salt of 16 bytes long
        # it should be 24 characters long in base-64
        salt_b64 = generate_salt(16)
        self.assertEqual(24, len(salt_b64))

    def test_generate_salt_12_base64(self):
        # When I generate a salt of 12 bytes long
        # it should be 16 characters long in base-64
        salt_b64 = generate_salt(12)
        self.assertEqual(16, len(salt_b64))

    def test_generate_salt_12_bytes(self):
        # When I generate a salt of 12 bytes long
        # it should be 12 bytes long
        salt_bytes = generate_salt(12, True)
        self.assertEqual(12, len(salt_bytes))

    # get_id

    def test_get_id_test1(self):
        # When I get_id 'Hello world'
        # it should be 16 characters long in base-64
        id_b64 = get_id('Hello world')
        self.assertEqual(16, len(id_b64))
        self.assertEqual(b'fA56zTvWu8DyuWx7', id_b64)

    def test_get_id_test1_bytes(self):
        # When I get_id 'Hello world' as bytes
        # it should be 12 bytes long by default
        id_bytes = get_id('Hello world', as_bytes=True)
        self.assertEqual(12, len(id_bytes))

    def test_get_id_test1_16(self):
        # When I get_id 'Hello world'
        # it should be 16 characters long in base-64
        id_b64 = get_id('Hello world', kdf_length=16)
        self.assertEqual(24, len(id_b64))
        self.assertEqual(b'fA56zTvWu8DyuWx7Q0tHZg==', id_b64)

    def test_get_id_test1_16_bytes(self):
        # When I get_id 'Hello world' as bytes
        # it should be 12 bytes long by default
        id_bytes = get_id('Hello world', kdf_length=16, as_bytes=True)
        self.assertEqual(16, len(id_bytes))

if __name__ == '__main__':
    pass
    #unittest.main()
