import typing

import cerberus  # type: ignore
import core.db.dynamodb


class User(typing.TypedDict):
    user_id: str
    user_name: str
    hashed_password: str


def connect_table(dynamodb: core.db.dynamodb.DynamoDB) -> core.db.dynamodb.Table:
    return core.db.dynamodb.connect_table(dynamodb, "User")


def from_item(item: core.db.dynamodb.Item) -> User:
    v = cerberus.Validator(
        {
            "UserId": {"type": "string", "required": True, "rename": "user_id"},
            "UserName": {"type": "string", "required": True, "rename": "user_name"},
            "HashedPassword": {
                "type": "string",
                "required": True,
                "rename": "hashed_password",
            },
        }
    )

    user = v.validated(item)
    if user is None:
        raise ValueError(v.errors)

    return typing.cast(User, user)


def to_item(user: User) -> core.db.dynamodb.Item:
    return {
        "UserId": user["user_id"],
        "UserName": user["user_name"],
        "HashedPassword": user["hashed_password"],
    }
