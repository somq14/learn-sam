import datetime
import typing
import uuid

import bcrypt
import core.datetime_util
import core.dynamodb
import db.session
import db.user

# initialize
dynamodb = core.dynamodb.connect_db()
user_table = db.user.connect_table(dynamodb)
session_table = db.session.connect_table(dynamodb)


class LoginServiceInput(typing.TypedDict):
    user_id: str
    password: str


class LoginServiceOutput(typing.TypedDict):
    user_id: str
    user_name: str
    session_id: str
    expires_at: datetime.datetime


class LoginServiceError(Exception):
    pass


class UserNotFoundError(LoginServiceError):
    pass


class BadCredentialError(LoginServiceError):
    pass


def login_service(input: LoginServiceInput) -> LoginServiceOutput:
    res = user_table.get_item(Key={"UserId": input["user_id"]})
    if "Item" not in res:
        raise UserNotFoundError({"user_id": input["user_id"]})
    user = db.user.from_item(res["Item"])

    # パスワードを検証する
    if not bcrypt.checkpw(
        password=input["password"].encode(),
        hashed_password=user["hashed_password"].encode(),
    ):
        raise BadCredentialError({"user_id": input["user_id"]})

    # セッションを作成し、DBに格納する
    now = core.datetime_util.now()
    session: db.session.Session = {
        "session_id": str(uuid.uuid4()),
        "user_id": user["user_id"],
        "authenticated_at": now,
        "expires_at": now + datetime.timedelta(hours=24),
    }
    # uuidは十分ランダムなためユニーク制約には違反しない
    session_table.put_item(Item=db.session.to_item(session))

    return {
        "user_id": user["user_id"],
        "user_name": user["user_name"],
        "session_id": session["session_id"],
        "expires_at": session["expires_at"],
    }
