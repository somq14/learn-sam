import os

import boto3
import mypy_boto3_dynamodb.service_resource


def get_table() -> mypy_boto3_dynamodb.service_resource.Table:
    dynamoEndpointUrl = os.getenv("DynamoDBEndpointUrl")
    dynamoTableName = os.getenv("DynamoDBTableName")
    if dynamoEndpointUrl is None or dynamoTableName is None:
        raise Exception("error")
    dynamodb = boto3.resource("dynamodb", endpoint_url=dynamoEndpointUrl)
    table = dynamodb.Table(dynamoTableName)
    return table
