import json
from typing import Any, Dict

import core.db.dynamodb
from boto3.dynamodb.conditions import Attr

dynamodb = core.db.dynamodb.connect_table()


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
