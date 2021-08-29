#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from app_helper import get_deployment_type, get_stack_config, get_cdk_defaults
from cdk.aws_stack import DanaTradingBotStack


app = core.App()

deployment_type=get_deployment_type(app.node)

stack_config=get_stack_config(deployment_type)

(cdk_default_account, cdk_default_region) = get_cdk_defaults(app.node, stack_config, deployment_type)

danaTradingBotStack = DanaTradingBotStack(app, "DanaTradingBotStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=core.Environment(account=cdk_default_account, region=cdk_default_region),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

# Add tags
# Add application-wide tags
core.Tags.of(app).add("app", "dana_trading_bot")

# Add stack-wide tags
core.Tags.of(danaTradingBotStack).add("stack-name", "DanaTradingBotStack");

app.synth()
