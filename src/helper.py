import datetime
import json
import uuid

class Helper:
    # Returns a JSON error with statusCode 403 and a custom message.
    def json_error(self, message):
        return {
            "statusCode": 403,
            "body": json.dumps({"message": message})
        }

    # Returns a JSON success message with a custom body
    def json_success(self, body=""):
        return {
            "statusCode": 200,
            "body": body
        }
    
    def create_id(self):
        return str(uuid.uuid4())

    def get_timestamp(self):
        return str(datetime.datetime.now())
