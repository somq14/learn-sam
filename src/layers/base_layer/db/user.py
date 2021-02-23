import typing

import cerberus  # type: ignore
import core.dynamodb


class User(typing.TypedDict):
    user_id: str
    user_name: str
    hashed_password: str


def connect_table(dynamodb: core.dynamodb.DynamoDB) -> core.dynamodb.Table:
    return core.dynamodb.connect_table(dynamodb, "User")


def from_item(item: core.dynamodb.Item) -> User:
    validator = cerberus.Validator(
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

    user = validator.validated(item)
    if user is not None:
        raise Exception()

    return typing.cast(User, user)


def to_item(user: User) -> core.dynamodb.Item:
    return {
        "UserId": user["user_id"],
        "UserName": user["user_name"],
        "HashedPassword": user["hashed_password"],
    }
