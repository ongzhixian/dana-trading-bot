import unittest

# https://realpython.com/api-integration-in-python/

class TestTelegram(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    #unittest.main()
    import requests
    # sendMessage
    api_url = "https://jsonplaceholder.typicode.com/todos"
    todo = {"userId": 1, "title": "Buy milk", "completed": False}
    response = requests.post(api_url, json=todo)
    #response.json()
    print(rsponse)
