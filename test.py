import boto3
import logging
import sys
import json
import botocore
import requests
import os
import yaml

pwd = os.path.dirname(os.path.realpath(__file__))

def load_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            line = line.rstrip() #removes trailing whitespace and '\n' chars

            if "=" not in line: continue #skips blanks and comments w/o =
            if line.startswith("#"): continue #skips comments which contain =

            k, v = line.split("=", 1)
            config[k] = v.replace("\"","")
    return config

def make_cloudformation_client(config=None):
    """
    this method will attempt to make a boto3 client
    it manages the choice for a custom config
    """
    #load the app config
    client = None
    if config != None:
        logging.info("using custom config.")
        config = load_config(config)
        client = boto3.client('cloudformation',
            config["AWS_REGION_NAME"],
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"])
    else:
        # we dont have a configuration, lets use the
        # standard configuration fallback
        logging.info("using default config.")
        client = boto3.client('cloudformation')
    if not client:
            raise ValueError('Not able to initialize boto3 client with configuration.')
    else:
            return client

def get_json(url, data_obj=None):
    r = requests.get(url)
    print(r.json())
    return r

def get_file(file_location):
    with open(file_location) as file_object:
        file = file_object.read()
    return file

def cfCreateStack(client,name,templatefile,params):
    #'name 'the name of the stack to create.') required
    #'--templatefile required=True 'the url where the stack template can be fetched.')
    #--params', required=True,'the key value pairs for the parameters of the stack.')
    #--topicarn', required=True,'the SNS topic arn for notifications to be sent to.')
    #--log', default="INFO", required=False,which log level. DEBUG, INFO, WARNING, CRITICAL')

    # init LOGGER
    #logging.basicConfig(level=get_log_level(log), format=LOG_FORMAT)


    try:

        response = client.create_stack(
            StackName=name,
            TemplateBody=get_file(templatefile), #template_object, #json.dumps(template_object),
            Parameters=params,
            DisableRollback=False,
            TimeoutInMinutes=2
        )

        # we expect a response, if its missing on non 200 then show response
        if 'ResponseMetadata' in response and \
            response['ResponseMetadata']['HTTPStatusCode'] < 300:
            logging.info("succeed. response: {0}".format(json.dumps(response)))
        else:
            logging.critical("There was an Unexpected error. response: {0}".format(json.dumps(response)))

    
    except ValueError as e:
        print(e)
        logging.critical("Value error caught: {0}".format(e))
    except botocore.exceptions.ClientError as e:
        print(e)
        logging.critical("Boto client error caught: {0}".format(e))
    except Exception as e:
        # catch any failure
        print(e)
        logging.critical("Unexpected error: {0}".format(sys.exc_info()[0]))
    



stack_params = [
    {
        'ParameterKey': 'KeyName',
        'ParameterValue': 'AxiadKey'
    },
    {
        'ParameterKey': 'VpcCidr',
        'ParameterValue': '10.1.0.0/16'
    },
    {
        'ParameterKey': 'InstanceType',
        'ParameterValue': 't2.micro'
    }
]


boto_client = make_cloudformation_client()
print(boto_client)
cfCreateStack(boto_client,"test",os.path.join(pwd,"asg_test.yaml"),
stack_params)