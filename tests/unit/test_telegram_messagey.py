import unittest
import json
import requests

def get_test_message():
    with open('tests/data/sample_telegram_update_message.json', "r") as in_file:
        json_str = in_file.read()
        return json.loads(json_str)

def send_message(chat_id, message):
    with open('app-secrets.json', "r") as in_file:
        secrets = json.loads(in_file.read())
    token = secrets['botToken']

    methodName = "sendMessage"
    api_url = f"https://api.telegram.org/bot{token}/{methodName}"
    message_headers =  {
        "Content-Type" : "application/json"
    }
    message_body = json.dumps({
        "chat_id" : chat_id,
        "text" : message
    })
    response = requests.post(api_url, headers=message_headers, data=message_body)
    response.json()

class TestTelegramMessage(unittest.TestCase):

    # def test_parse(self):
    #     msg = get_test_message()
    #     self.assertEqual('foo'.upper(), 'FOO')

    def test_send_message(self):
        with open('app-secrets.json', "r") as in_file:
            secrets = json.loads(in_file.read())
        token = secrets['botToken']
        send_message(53274105, 'Trading indicator\nplaning trades')

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
    