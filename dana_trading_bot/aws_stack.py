from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    # aws_sqs as sqs,
    # aws_sns as sns,
    # aws_sns_subscriptions as subs,
    # aws_lambda_event_sources as lambda_event_source,
    aws_lambda as lambda_,
    aws_apigateway as api_gateway,
    core
)


class DanaTradingBotStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # S3 buckets
        # DynamoDB tables
        # SQS queues
        # SNS topics
        # Lambda functions
        # REST API Gateway 

        # The code that defines your stack goes here

        # Define the Lambda functions that we will create here

        dana_update_handler = lambda_.Function(
            self, 'UpdateMessageHandler',
            function_name="dana_update_handler",
            description="Dana bot update message handler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            code=lambda_.Code.asset('lambdaFunctions'),
            handler='telegram_bot.update_handler',
        )

        # REST API Gateway

        api_gateway.LambdaRestApi(
            self, 'dana_update_message_endpoint',
            description="Dana bot update messages endpoint",
            handler=dana_update_handler,
        )
