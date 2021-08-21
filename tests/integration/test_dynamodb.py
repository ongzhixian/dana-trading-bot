import unittest
import boto3
from boto3.dynamodb.types import Binary, Decimal
import requests
import warnings

from mods.ddb import store

class TestDdb(unittest.TestCase):

    mock_data = {
        'RESPONSE_METADATA' : {
            'ResponseMetadata': {
                'RequestId': '75N4RS5BDFE4NGOK864RHBFBH7VV4KQNSO5AEMVJF66Q9ASUAAJG', 
                'HTTPStatusCode': 200, 
                'HTTPHeaders': {
                    'server': 'Server', 
                    'date': 'Sat, 21 Aug 2021 13:07:47 GMT', 
                    'content-type': 'application/x-amz-json-1.0', 
                    'content-length': '2', 
                    'connection': 'keep-alive', 
                    'x-amzn-requestid': '75N4RS5BDFE4NGOK864RHBFBH7VV4KQNSO5AEMVJF66Q9ASUAAJG', 
                    'x-amz-crc32': '2745614147'
                }, 
                'RetryAttempts': 0
            }
        },
        'PLAIN_TEXT_ITEM' : {
            'id' : 'sample7',
            "Author": "William Shakespeare", 
            "Title": "Romeo",
            "Category": "Drama"
        },
        'RETRIEVE_ITEM' : {
            'Item': {
                'info': {
                    'rating': Decimal('3'), 
                    'plot': 'awful'
                }, 
                'app': {
                    'name': 'some generic app', 
                    'version': Decimal('10')
                }, 
                'and some binary': Binary(b'\x00\x01\x02'), 
                'year': Decimal('2021'), 
                'comment': 'alone', 
                'some numbers': Decimal('99'), 
                'id': 'enc2', 
                'title': 'my horrible movie', 
                'example': 'data'
            }, 
            'ResponseMetadata': {
                'RequestId': 'OBKNV1BON1MCPUDFVS0A1LC513VV4KQNSO5AEMVJF66Q9ASUAAJG', 
                'HTTPStatusCode': 200, 
                'HTTPHeaders': {
                    'server': 'Server', 
                    'date': 'Sat, 21 Aug 2021 14:19:31 GMT', 
                    'content-type': 'application/x-amz-json-1.0', 
                    'content-length': '308', 'connection': 'keep-alive', 
                    'x-amzn-requestid': 'OBKNV1BON1MCPUDFVS0A1LC513VV4KQNSO5AEMVJF66Q9ASUAAJG', 
                    'x-amz-crc32': '1593809059'
                }, 
                'RetryAttempts': 0
            }
        }
    }

    def test_store_data(self):

        warnings.simplefilter("ignore", ResourceWarning)

        # Arrange

        plaintext_item = self.mock_data['PLAIN_TEXT_ITEM']
        plaintext_item['id'] = 'TEST_DATA_1'

        dynamodb = boto3.resource('dynamodb')

        dana_table = dynamodb.Table('dana_table')
        
        # Act
        response = store(dana_table, plaintext_item)

        response_metadata = None

        if 'ResponseMetadata' in response:
            response_metadata = response['ResponseMetadata']
            
        if 'HTTPStatusCode' in response_metadata:
            http_status_code = response_metadata['HTTPStatusCode']

        # Assert(s)

        self.assertIsNotNone(response_metadata)
        self.assertEqual(200, http_status_code)

    def test_store_encrypted_data(self):

        warnings.simplefilter("ignore", ResourceWarning)

        # Arrange

        plaintext_item = self.mock_data['PLAIN_TEXT_ITEM']
        plaintext_item['id'] = 'TEST_DATA_2'

        dynamodb = boto3.resource('dynamodb')

        dana_table = dynamodb.Table('dana_table')
        
        # Act
        response = store(dana_table, plaintext_item, encrypt=True)

        response_metadata = None

        if 'ResponseMetadata' in response:
            response_metadata = response['ResponseMetadata']
            
        if 'HTTPStatusCode' in response_metadata:
            http_status_code = response_metadata['HTTPStatusCode']

        # Assert(s)

        self.assertIsNotNone(response_metadata)
        self.assertEqual(200, http_status_code)

if __name__ == '__main__':
    unittest.main()
    