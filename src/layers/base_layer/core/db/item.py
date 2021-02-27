import typing
from datetime import datetime

import cerberus  # type: ignore
import core.db.dynamodb
import core.util.datetime_util


class Item(typing.TypedDict):
    user_id: str
    created_at: datetime
    content: str


def connect_table(dynamodb: core.db.dynamodb.DynamoDB) -> core.db.dynamodb.Table:
    return core.db.dynamodb.connect_table(dynamodb, "Item")


def from_item(item: core.db.dynamodb.Item) -> Item:
    v = cerberus.Validator(
        {
            "UserId": {"type": "string", "required": True, "rename": "user_id"},
            "CreatedAt": {
                "type": "datetime",
                "required": True,
                "coerce": core.util.datetime_util.parse,
                "rename": "created_at",
            },
            "Content": {
                "type": "string",
                "required": True,
                "rename": "content",
            },
        }
    )

    item = v.validated(item)
    if item is None:
        raise ValueError(v.errors)

    return typing.cast(Item, item)


def to_item(item: Item) -> core.db.dynamodb.Item:
    return {
        "UserId": item["user_id"],
        "CreatedAt": item["created_at"],
        "Content": item["content"],
    }
