import json
import os
from helper import Helper
import boto3


def handler(event, context):
    environment = os.environ["ENVIRONMENT"]
    dynamo_url = os.environ["DYNAMO_URL"]
    TABLE_NAME = os.environ["TABLE_NAME"]

    help = Helper()

    if environment == "dev":
        dynamo = boto3.resource("dynamodb", endpoint_url=dynamo_url)
    else:
        dynamo = boto3.resource("dynamodb")

    pk = event["pathParameters"]["pk"]
    # # Validate the json payload
    # if not hlp.validate_payload(request_body):
    #     return hlp.json_error("Validation failed!")

    table = dynamo.Table(TABLE_NAME)

    query = table.delete_item(
        Key={
            'id': pk
        }
    )

    print("HERERERE*******\n")
    print(query)

    if query["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return help.json_success("Deleted item {}".format(pk))
    else:
        return help.json_error("An error occurred. The item could not be created!")
