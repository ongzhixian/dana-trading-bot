import boto3
from boto3.dynamodb.types import Binary
from dynamodb_encryption_sdk.encrypted.table import EncryptedTable
from dynamodb_encryption_sdk.identifiers import CryptoAction
from dynamodb_encryption_sdk.material_providers.aws_kms import AwsKmsCryptographicMaterialsProvider
from dynamodb_encryption_sdk.structures import AttributeActions

def get_encrypted_table(dynamodb_table, custom_attribute_actions=None):
    aws_cmk_arn = 'arn:aws:kms:us-east-1:009167579319:key/0b6f4c23-da9a-4e92-bc58-87c600e0f23d'
    aws_kms_cmp = AwsKmsCryptographicMaterialsProvider(key_id=aws_cmk_arn)

    # Create attribute actions that tells the encrypted table to encrypt all attributes except one.
    actions = AttributeActions(
        default_action=CryptoAction.ENCRYPT_AND_SIGN, 
        attribute_actions={
            "comment": CryptoAction.DO_NOTHING, 
            "info": CryptoAction.DO_NOTHING
        }
    )
    # Use these objects to create an encrypted table resource.
    encrypted_table = EncryptedTable(table=dynamodb_table, materials_provider=aws_kms_cmp, attribute_actions=actions)
    return encrypted_table
    
def store(dynamodb_table, dynamodb_item, encrypt=False):
    if encrypt:
        return get_encrypted_table(dynamodb_table).put_item(Item=dynamodb_item)
        
    return dynamodb_table.put_item(Item=dynamodb_item)


def retrieve(dynamodb_table, dynamodb_key, encrypt=False):
    if encrypt:
        return get_encrypted_table(dynamodb_table).get_item(Key=dynamodb_key)
    return dynamodb_table.get_item(Key=dynamodb_key)

def remove(dynamodb_table, dynamodb_key):
    return dynamodb_table.delete_item(Key=dynamodb_key)


# def store_encrypted(dynamodb_table, dynamodb_item):
#     encrypted_table = get_encrypted_table(dynamodb_table)   # Use this if we are storing encrypted data
#     encrypted_table.put_item(dynamodb_item)


def demo(dynamodb_table, dynamodb_item, encrypt=False):
    return "DEMO1"
