import json
import os
from typing import Any, Dict

import boto3

dynamoEndpointUrl = os.getenv("DynamoDBEndpointUrl")
dynamoTableName = os.getenv("DynamoDBTableName")
if dynamoEndpointUrl is None or dynamoTableName is None:
    raise Exception("error")

dynamodb = boto3.resource("dynamodb", endpoint_url=dynamoEndpointUrl)
table = dynamodb.Table(dynamoTableName)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    item_id = event["pathParameters"]["item_id"]

    try:
        res = table.get_item(
            Key={
                "PK": item_id,
                "SK": item_id,
            }
        )

        if "Item" not in res:
            return {
                "statusCode": 404,
                "body": json.dumps({}),
            }

        item = res["Item"]
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "id": item["PK"],
                    "title": item["title"],
                }
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "internal server error"}),
        }
