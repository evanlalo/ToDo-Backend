from time import sleep
import boto3
import sys
import os
import uuid
import setup
import datetime

TABLE_NAME = os.environ["TABLE_NAME"]

# Create the course_subscriptions table in the database.
def create_table(resource=None):
    if not dynamodb:
        resource = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

    table = resource.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
            {"AttributeName": "created_on", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "created_on", "AttributeType": "S"},
            # {"AttributeName": "description", "AttributeType": "S"},
        ],
        # LocalSecondaryIndexes=[
        #     {
        #         "IndexName": "vin_status",
        #         "KeySchema": [
        #             {"AttributeName": "vin", "KeyType": "HASH"},
        #             {"AttributeName": "status", "KeyType": "RANGE"},
        #         ],
        #         "Projection": {
        #             "ProjectionType": "ALL",
        #         },
        #     },
        # ],
        # GlobalSecondaryIndexes=[
        #     {
        #         "IndexName": "rooftop_id-index",
        #         "KeySchema": [
        #             {"AttributeName": "rooftop_id", "KeyType": "HASH"},
        #         ],
        #         "Projection": {
        #             "ProjectionType": "ALL",
        #         },
        #         "ProvisionedThroughput": {
        #             "ReadCapacityUnits": 10,
        #             "WriteCapacityUnits": 10,
        #         },
        #     },
        #     {
        #         "IndexName": "status-index",
        #         "KeySchema": [
        #             {"AttributeName": "status", "KeyType": "HASH"},
        #         ],
        #         "Projection": {
        #             "ProjectionType": "ALL",
        #         },
        #         "ProvisionedThroughput": {
        #             "ReadCapacityUnits": 10,
        #             "WriteCapacityUnits": 10,
        #         },
        #     },
        # ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )

    return table


# Delete the course_subscriptions table in the database
def delete_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    try:
        table = dynamodb.Table(TABLE_NAME)
        table.delete()
        return "Table has been deleted"
    except:
        return "Table wasn't found"


# Add an item to the course_subscriptions table
def add_item_to_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)
    added_item = table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "created_on": str(datetime.datetime.today()),
            "task": "Buy milk",
        }
    )
    return added_item


# Scans the course_subscriptions table for all entries
def get_items_from_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://127.0.0.1:8000")

    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    data = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    return data


def get_table_status():
    dynamodb_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

    return dynamodb_client.describe_table(TableName=TABLE_NAME)


if __name__ == "__main__":

    # Get the first parameter provided on the command line when executing the script.
    cmd = sys.argv[1]

    # Create the dynamodb object
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    # Execute the function based on provided first argument when executing the script.
    if cmd == "create":
        table = create_table(dynamodb)
        print(table.table_status)
        print("Table status:", table.table_status)
    elif cmd == "delete":
        message = delete_table(dynamodb)
        print("Status: ", message)
    elif cmd == "add":
        added_item = add_item_to_table(dynamodb)
        print("Added Item:", added_item)
    elif cmd == "list":
        items_list = get_items_from_table(dynamodb)
        print("Items List:", items_list)
    elif cmd == "status":
        table = get_table_status()
        print("Table:", table)