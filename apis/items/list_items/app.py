import json
import os
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource(
    "dynamodb", endpoint_url=os.getenv("DynamoDBEndpointUrl"))
table = dynamodb.Table(os.getenv("DynamoDBTableName"))


def lambda_handler(event, context):
    try:
        res = table.scan(
            Limit=100,
            FilterExpression=Attr("title").exists())

        items = list(map(lambda item: {
            "id": item["PK"],
            "title": item["title"]
        }, res["Items"]))

        return {
            "statusCode": 200,
            "body": json.dumps({
                "items": items
            })
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "internal server error"})
        }