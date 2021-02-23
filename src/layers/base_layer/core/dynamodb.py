import os
from decimal import Decimal
from typing import Any, Dict, List, Set, Union

import boto3
import mypy_boto3_dynamodb.service_resource

# 型定義
DynamoDB = mypy_boto3_dynamodb.service_resource.DynamoDBServiceResource
Table = mypy_boto3_dynamodb.service_resource.Table
Item = Dict[
    str,
    Union[
        bytes,
        bytearray,
        str,
        int,
        Decimal,
        bool,
        Set[int],
        Set[Decimal],
        Set[str],
        Set[bytes],
        Set[bytearray],
        List[Any],
        Dict[str, Any],
        None,
    ],
]


def connect_db() -> DynamoDB:
    dynamoEndpointUrl = os.getenv("DynamoDBEndpointUrl")
    if dynamoEndpointUrl is None:
        raise Exception("error")

    dynamodb = boto3.resource("dynamodb", endpoint_url=dynamoEndpointUrl)
    return dynamodb


def connect_table(dynamodb: DynamoDB, table_name: str) -> Table:
    # suffix
    dynamodb_table_name = os.getenv("DynamoDBTableName")
    if dynamodb_table_name is None:
        raise Exception("error")
    table = dynamodb.Table(dynamodb_table_name + table_name)
    return table


def get_table() -> Table:
    dynamoEndpointUrl = os.getenv("DynamoDBEndpointUrl")
    dynamoTableName = os.getenv("DynamoDBTableName")
    if dynamoEndpointUrl is None or dynamoTableName is None:
        raise Exception("error")
    dynamodb = boto3.resource("dynamodb", endpoint_url=dynamoEndpointUrl)
    table = dynamodb.Table(dynamoTableName)
    return table
