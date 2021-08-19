import json
import os
  

def update_handler(event, context):
    #print('request: {}'.format(json.dumps(event)))
    telegram_message = json.loads(event['body'])
    print('request: {}'.format(json.dumps(telegram_message)))
    
    chat_id = telegram_message['message']['chat']['id']
    message_text = telegram_message['message']['text']
    print(f'chat_id: {chat_id}')
    print(f'message_text: {message_text}')

    # Test getting environment variable
    prd_db_url = os.environ['production_db_url']
    dev_db_url = os.environ['development_db_url']

    print(f'prd_db_url: {prd_db_url}')
    print(f'dev_db_url: {dev_db_url}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }