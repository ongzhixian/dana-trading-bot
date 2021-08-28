import json
import logging

# Helper functions for app.py

def get_deployment_type(app_node, setting_name = 'deployment_type'):
    try:
        deployment_type = app_node.try_get_context(setting_name)

        if deployment_type is None:
            print(f"[ERROR]  Context flag '{setting_name}' not found.")
            print(f"         Please add context flag '--context {setting_name}=<value:[dev|prd]>'")
            raise ValueError(setting_name, deployment_type)

        print(f"{setting_name}: [{deployment_type}]")
        return deployment_type

    except:
        raise


# def get_config_setting(cdk_config, setting_name):
#     if setting_name in cdk_config:
#         return cdk_config[setting_name]



def get_stack_config(deployment_type="dev"):
    try:
        with open('stack-config.json') as stack_config_file:
            stack_config_json = json.loads(stack_config_file.read())
    except:
        print("[ERROR]  Error opening 'stack-config.json' file or reading file content as json.")
        raise

    if deployment_type in stack_config_json:
        stack_config = stack_config_json[deployment_type]
        print(f"stack_config: [{stack_config}]")
        return stack_config
    
    print(f"[ERROR]  Value '{deployment_type}' for 'deployment_type' not found in 'stack-config.json'.")
    print(f"         Please add section '{deployment_type}' in 'stack-config.json'.")
    raise ValueError("deployment_type", deployment_type)
    

def get_cdk_defaults(app_node, stack_config, deployment_type):
    try:
        if 'cdk' in stack_config:
            cdk_stack_config = stack_config['cdk']
        else:
            print(f"[ERROR]  The section {deployment_type} in 'stack-config.json' is missing 'cdk' section.")
            print(f"         Please add 'cdk' section under '{deployment_type}' section in 'stack-config.json'.")
            raise ValueError("stack_config", stack_config)

        # The 3 ways of getting values for 'CDK_DEFAULT_ACCOUNT'
        # 1)    Context flag 
        # 2)    Configuration json file
        # 3)    Environment variables   # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
        
        setting_name = 'cdk_default_account'
        cdk_default_account = app_node.try_get_context(setting_name) or cdk_stack_config['default_account'] 
        if cdk_default_account is None:
            print(f"[ERROR]  '{setting_name}' is not defined.")
            print(f"         Please add  context flag '--context {setting_name}=<value:01234567>'")
            print(f"         -- OR --")
            print(f"         Please add '{setting_name}' key-value-pair in the 'cdk' section under '{deployment_type}' in 'stack-config.json'.")
            raise ValueError(setting_name, cdk_default_account)

        setting_name = 'cdk_default_region'
        cdk_default_region =  app_node.try_get_context(setting_name) or cdk_stack_config['default_region']
        if cdk_default_region is None:
            print(f"[ERROR]  '{setting_name}' is not defined")
            print(f"         Please add  context flag '--context {setting_name}=<value:[dev|prd]>'")
            print(f"         -- OR --")
            print(f"         Please add '{setting_name}' key-value-pair in the 'cdk' section under '{deployment_type}' in 'stack-config.json'.")
            raise ValueError(setting_name, cdk_default_account)

        print(f"cdk_default_account: [{cdk_default_account}]")
        print(f"cdk_default_region:  [{cdk_default_region}]")
        return (cdk_default_account, cdk_default_region)
    except:
        raise
