import json
import os
import boto3
from helper import Helper


def handler(event, context):
    environment = os.environ["ENVIRONMENT"]
    dynamo_url = os.environ["DYNAMO_URL"]
    TABLE_NAME = os.environ["TABLE_NAME"]

    # Create helper object (see helper.py)
    help = Helper()

    if environment == "dev":
        table = boto3.resource("dynamodb", endpoint_url=dynamo_url)
    else:
        table = boto3.resource("dynamodb")

    request_body = json.loads(event["body"])
    body = request_body
    # # Validate the json payload
    # if not hlp.validate_payload(request_body):
    #     return hlp.json_error("Validation failed!")

    # Execute create query on DynamoDB table
    table = table.Table(TABLE_NAME)

    item = {
        "id": help.create_id(),
        "created_on": help.get_timestamp(),
        "task": body["task"],
    }

    added_item = table.put_item(Item=item)

    # If DynamoDB could create the record, we will receive a 200 status code, and can return success.
    if added_item["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return help.json_success(request_body)
    else:
        return help.json_error("An error occurred. The item could not be created!")
