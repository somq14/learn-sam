import json
import os
from typing import Any, Dict

import boto3
from boto3.dynamodb.conditions import Attr

dynamoEndpointUrl = os.getenv("DynamoDBEndpointUrl")
dynamoTableName = os.getenv("DynamoDBTableName")
if dynamoEndpointUrl is None or dynamoTableName is None:
    raise Exception("error")

dynamodb = boto3.resource("dynamodb", endpoint_url=dynamoEndpointUrl)
table = dynamodb.Table(dynamoTableName)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        res = table.scan(Limit=100, FilterExpression=Attr("title").exists())

        items = list(
            map(lambda item: {"id": item["PK"], "title": item["title"]}, res["Items"])
        )

        return {"statusCode": 200, "body": json.dumps({"items": items})}
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "internal server error"}),
        }
