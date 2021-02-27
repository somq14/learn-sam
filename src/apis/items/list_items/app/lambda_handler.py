import json
from datetime import datetime
from typing import TypedDict

import core.api
import core.db.dynamodb
import core.db.item

dynamodb = core.db.dynamodb.connect_db()
item_table = core.db.item.connect_table(dynamodb)


class RequestParam(TypedDict):
    userId: str
    createdAt: datetime


@core.api.default_interceptor(access_control_allow_origin="http://localhost:3000")
def lambda_handler(
    event: core.api.Event, context: core.api.Context
) -> core.api.Response:
    print(event)

    event["queryStringParameters"]

    res = item_table.scan()

    items = list(
        map(lambda item: {"id": item["PK"], "title": item["title"]}, res["Items"])
    )

    return {"statusCode": 200, "body": json.dumps({"items": items})}
