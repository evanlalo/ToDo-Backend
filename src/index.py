import json
import boto3
import os
from helper import Helper


def handler(event, context):
    environment = os.environ['ENVIRONMENT']
    dynamo_url = os.environ['DYNAMO_URL']
    TABLE_NAME = os.environ["TABLE_NAME"]

    # Create helper object (see helper.py)
    help = Helper()

    if environment == "dev":
        dynamodb = boto3.resource('dynamodb', endpoint_url=dynamo_url)
    else:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    data = json.dumps(response['Items'])

    return help.json_success(data)
