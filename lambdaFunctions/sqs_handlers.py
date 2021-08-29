import boto3

# Create SQS client
sqs_client = boto3.client('sqs')

def sqs_test_message_dlq_handler(event, context):
    for record in event['Records']:
        print("sqs_test_message_dlq_handler")
        payload = record["body"]
        print(str(payload))
        # In the .NET code, when the dead-letter queue received a message, it expects the message to be a list of tradeIds strings


def get_queue_url(queue_name):
    try:
        response = sqs_client.get_queue_url(
            QueueName="dev-sqs-test-message"
        )
        # Response 'https://sqs.us-east-1.amazonaws.com/009167579319/dev-sqs-test-message'
        print(response)
        return response["QueueUrl"]
    except:
        raise


def send_message(queue_name, message_body, message_attributes):
    try:
        queue_url = get_queue_url(queue_name)

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        print(response)
    except: 
        raise

def enqueue_message(queue_name, message):
    pass
    message_attributes = message['messageAttributes']

    print(message_attributes)

    enqueue_count = 0
    if 'enqueue_count' in message_attributes:
        enqueue_count = int(message_attributes['enqueue_count']["stringValue"])
    
    enqueue_count = enqueue_count + 1

    print(f"enqueue_count: {enqueue_count}")

    message_attributes.update({
        'enqueue_count': {
            'StringValue': str(enqueue_count), 
            'DataType': 'Number'
        }
    })

    queue_url = get_queue_url(queue_name)

    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message["body"],
        MessageAttributes=message_attributes
    )

    return response
    

def sqs_test_message_handler(event, context):
    for record in event['Records']:
        print("sqs_test_message_handler")
        print(event)
        print(record)
        payload = record["body"]
        print(str(payload))
        if str(payload).startswith("ERROR"):
            # SQS move
            
            message_attributes = record['messageAttributes']

            print(message_attributes)

            retries_count = 0
            if 'retries_count' in message_attributes:
                retries_count = int(message_attributes['retries_count']["stringValue"])
            
            retries_count = retries_count + 1

            print(f"retries_count: {retries_count}")

            message_attributes.update({
                'retries_count': {
                    'StringValue': str(retries_count), 
                    'DataType': 'Number'
                }
            })

            if retries_count <= 5:
                pass
                # Resend to the same queue
                #send_message("dev-sqs-test-message", record["body"], message_attributes)

            # ZX: Raising an Exception has no meaning except where logs are concern
            raise Exception("payload has error")
            # response = sqs.send_message(
            #     QueueUrl=queue_url,
            #     DelaySeconds=10,
            #     MessageAttributes={
            #         'Title': {
            #             'DataType': 'String',
            #             'StringValue': 'The Whistler'
            #         },
            #         'Author': {
            #             'DataType': 'String',
            #             'StringValue': 'John Grisham'
            #         },
            #         'WeeksOn': {
            #             'DataType': 'Number',
            #             'StringValue': '6'
            #         }
            #     },
            #     MessageBody=(
            #         'Information about current NY Times fiction bestseller for '
            #         'week of 12/11/2016.'
            #     )
            # )
            # # SQS.send_message(
            # # QueueUrl=config.SQS_MAIN_URL,
            # # MessageBody=record['body'],
            # # DelaySeconds=int(delaySeconds),
            # # MessageAttributes=record['messageAttributes']
            # # )
            # Don't raise Exception; 
            # raise Exception("payload has error")
