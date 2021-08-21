import json
import os
  

def update_handler(event, context):
    #print('request: {}'.format(json.dumps(event)))
    telegram_message = json.loads(event['body'])
    print('request: {}'.format(json.dumps(telegram_message)))
    
    if 'message' in telegram_message:
        received_message = telegram_message['message']
    elif 'edited_message' in telegram_message:
        received_message = telegram_message['edited_message']
    elif 'channel_post' in telegram_message:
        received_message = telegram_message['channel_post']
    elif 'edited_channel_post' in telegram_message:
        received_message = telegram_message['edited_channel_post']

    chat_id = received_message['chat']['id']
    print(f'chat_id: {chat_id}')

    if 'text' in received_message:
        print('in received_message')
        message_text = received_message['text']
        print(f'message_text: {message_text}')
    else:
        print('UNRECOGNISE MESSAGE TYPE ')

    # Test getting environment variable
    # prd_db_url = os.environ['production_db_url']
    # dev_db_url = os.environ['development_db_url']
    # print(f'prd_db_url: {prd_db_url}')
    # print(f'dev_db_url: {dev_db_url}')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }