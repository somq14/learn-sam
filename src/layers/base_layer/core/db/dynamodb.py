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


class DynamoDBConfigurationError(Exception):
    pass


def connect_db() -> DynamoDB:
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL")
    if endpoint_url is None:
        raise DynamoDBConfigurationError("DYNAMODB_ENDPOINT_URL")
    return boto3.resource("dynamodb", endpoint_url=endpoint_url)


def connect_table(dynamodb: DynamoDB, table_name: str) -> Table:
    table_name_suffix = os.getenv("DYNAMODB_TABLE_NAME_SUFFIX")
    if table_name_suffix is None:
        raise DynamoDBConfigurationError("DYNAMODB_TABLE_NAME_SUFFIX")
    return dynamodb.Table(table_name + table_name_suffix)
