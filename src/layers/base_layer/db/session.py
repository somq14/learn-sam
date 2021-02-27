import datetime
import typing

import cerberus  # type: ignore
import core.datetime_util
import core.dynamodb


class Session(typing.TypedDict):
    session_id: str
    user_id: str
    authenticated_at: datetime.datetime
    expires_at: datetime.datetime


def connect_table(dynamodb: core.dynamodb.DynamoDB) -> core.dynamodb.Table:
    return core.dynamodb.connect_table(dynamodb, "Session")


def from_item(item: core.dynamodb.Item) -> Session:
    v = cerberus.Validator(
        {
            "SessionId": {"type": "string", "required": True, "rename": "session_id"},
            "UserId": {
                "type": "string",
                "required": True,
                "rename": "user_id",
            },
            "AuthenticatedAt": {
                "type": "datetime",
                "coerce": core.datetime_util.parse,
                "required": True,
                "rename": "authenticated_at",
            },
            "ExpiresAt": {
                "type": "string",
                "coerce": core.datetime_util.parse,
                "required": True,
            },
        }
    )
    session = v.validated(item)
    if session is None:
        raise ValueError(v.errors)

    return typing.cast(Session, session)


def to_item(session: Session) -> core.dynamodb.Item:
    return {
        "SessionId": session["session_id"],
        "UserId": session["user_id"],
        "AuthenticatedAt": core.datetime_util.format(session["authenticated_at"]),
        "ExpiresAt": core.datetime_util.format(session["expires_at"]),
    }
