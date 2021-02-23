import datetime
import uuid
from typing import Any, TypedDict

import bcrypt
import core.dynamodb
import db.session
import db.user

# initialize
dynamodb = core.dynamodb.connect_db()
user_table = db.user.connect_table(dynamodb)
session_table = db.session.connect_table(dynamodb)


class AppException(Exception):
    pass


class InconsistentDataException(Exception):
    def __init__(self, cause: Any):
        self.cause = cause


class UserNotFoundException(AppException):
    pass


class BadCredentialException(AppException):
    pass


class LoginServiceInput(TypedDict):
    user_id: str
    password: str


class LoginServiceOutput(TypedDict):
    session_id: str


def login_service(input: LoginServiceInput) -> LoginServiceOutput:
    res = user_table.get_item(Key={"UserId": input["user_id"]})
    if res["Item"] is None:
        raise UserNotFoundException()

    user = db.user.from_item(res["Item"])

    # パスワードを検証する
    if not bcrypt.checkpw(
        password=input["password"].encode(),
        hashed_password=user["hashed_password"].encode(),
    ):
        raise BadCredentialException()

    # セッションを作成し、DBに格納する
    session_id = str(uuid.uuid4())

    authenticated_at = datetime.datetime.now(datetime.timezone.utc)
    expire_at = authenticated_at + datetime.timedelta(hours=24)

    session_table.put_item(
        Item={
            "SessionId": session_id,
            "UserId": user["user_id"],
            "AuthenticatedAt": authenticated_at.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "ExpireAt": expire_at.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        }
    )

    return {"session_id": session_id}
