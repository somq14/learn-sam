import datetime
import typing

import cerberus  # type: ignore
import core.datetime_util
import core.dynamodb


class Session(typing.TypedDict):
    session_id: str
    user_id: str
    authenticated_at: datetime.datetime
    expire_at: datetime.datetime


schema = {
    "session": {"type": "string", "required": True},
    "user_id": {"type": "string", "required": True},
    "authenticated_at": {"type": "datetime", "required": True},
    "expire_at": {"type": "datetime", "required": True},
}


def connect_table(dynamodb: core.dynamodb.DynamoDB) -> core.dynamodb.Table:
    return core.dynamodb.connect_table(dynamodb, "Session")


def from_item(item: core.dynamodb.Item) -> Session:
    session = {
        "session_id": item.get(""),
        "user_id": item.get("UserId"),
        "authenticated_at": item.get("AuthenticatedAt"),
        "expire_at": item.get("ExpireAt"),
    }

    validator = cerberus.Validator(schema)
    if not validator.validate():
        raise Exception()

    return typing.cast(Session, session)


def to_item(session: Session) -> core.dynamodb.Item:
    return {
        "SessionId": session["session_id"],
        "UserId": session["user_id"],
        "AuthenticatedAt": core.datetime_util.format(session["authenticated_at"]),
        "ExpireAt": core.datetime_util.format(session["expire_at"]),
    }
