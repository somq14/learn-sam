import json
from typing import Any, Dict

import common.dynamodb


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    table = common.dynamodb.get_table()
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
