import json

from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    # aws_sns as sns,
    # aws_sns_subscriptions as subs,
    # aws_lambda_event_sources as lambda_event_source,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_apigateway as api_gateway,
    aws_kms as kms,
    aws_dynamodb as dynamodb,
    core
)


class DanaTradingBotStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Define KMS CMS
        # S3 buckets
        # DynamoDB tables
        # SQS queues
        # SNS topics
        # Lambda functions
        # REST API Gateway 

        with open("app-config.json", "r") as in_file:
            config = json.loads(in_file.read())

        print("production_db_url: {}".format(config['production_db_url']))
        print("development_db_url: {}".format(config['development_db_url']))

        # The code that defines your stack goes here

        # Define KMS CMS
        
        # kms.Key(self, 'dynamoDbConfig', 
        #     alias="dynamoDbConfig",
        #     description="Key for DynamoDB secrets"
        # )

        # DynamoDB tables

        dana_table = dynamodb.Table(
            self, "dana_table",
            table_name="dana_table",
            read_capacity=5,
            write_capacity=5,
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )

        ## SQS queues

        sqs_test_message_dlq = sqs.Queue(
            self, "dev-sqs-test-message-dlq",
            queue_name = "dev-sqs-test-message-dlq",
            visibility_timeout=core.Duration.seconds(300),
            #encryption=
            #encryption_master_key=
        )
        #dlq_messages_handler.add_event_source(lambda_event_source.SqsEventSource(poc_dead_letter_queue))

        sqs_test_message = sqs.Queue(
            self, "dev-sqs-test-message",
            queue_name = "dev-sqs-test-message",
            visibility_timeout=core.Duration.seconds(300),
            dead_letter_queue=sqs.DeadLetterQueue( max_receive_count=5, queue=sqs_test_message_dlq )
            #encryption=
            #encryption_master_key=
        )

        # sqs_event_source = lambda_event_source.SqsEventSource(poc_queue)
        # trade_message_handler.add_event_source(sqs_event_source)


        # Define the Lambda functions that we will create here

        dana_update_handler = lambda_.Function(
            self, 'UpdateMessageHandler',
            function_name="dana_update_handler",
            description="Dana bot update message handler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            code=lambda_.Code.asset('lambdaFunctions'),
            handler='telegram_bot.update_handler',
            environment={ # ADD THIS, FILL IT FOR ACTUAL VALUE 
                "production_db_url": config['production_db_url'],
                "development_db_url": config['development_db_url']
            }
        )

        # REST API Gateway

        api_gateway.LambdaRestApi(
            self, 'dana_update_message_endpoint',
            description="Dana bot update messages endpoint",
            handler=dana_update_handler,
        )

        # SNS topics

        # topic = sns.Topic(
        #     self, "dev-sns-pocAwsPython", 
        #     topic_name="dev-sns-pocAwsPython"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))

        core.CfnOutput(self, "sqs_test_message",
            value=sqs_test_message.queue_url,
            description="asdads",
            export_name="sqs-test-message-queue-url"
        )
