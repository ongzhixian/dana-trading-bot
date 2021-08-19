import unittest
import json

def get_test_message():
    with open('tests/data/sample_telegram_update_message.json', "r") as in_file:
        json_str = in_file.read()
        return json.loads(json_str)

class TestTelegramMessage(unittest.TestCase):

    def test_parse(self):
        msg = get_test_message()
        import pdb
        pdb.set_trace()
        self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()
    # msg = get_test_message()
    