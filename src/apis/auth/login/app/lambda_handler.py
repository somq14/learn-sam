import json
from typing import TypedDict

import core.api

from . import service


class RequestBody(TypedDict):
    userId: str
    password: str


class ResponseBody(TypedDict):
    userId: str
    userName: str


@core.api.default_interceptor()
def lambda_handler(
    event: core.api.Event,
    context: core.api.Context,
) -> core.api.Response:

    req_body: RequestBody = core.api.decode_request_body(
        event["body"],
        {
            "userId": {"type": "string", "required": True},
            "password": {"type": "string", "required": True},
        },
    )

    input: service.LoginServiceInput = {
        "user_id": req_body["userId"],
        "password": req_body["password"],
    }
    output = service.login_service(input)

    res_body: ResponseBody = {
        "userId": output["user_id"],
        "userName": output["user_name"],
    }

    return {
        "statusCode": 200,
        "headers": {
            "Set-Cookie": "; ".join(
                [
                    "Id={}".format(output["session_id"]),
                    "Secure",
                    "HttpOnly",
                ]
            )
        },
        "body": json.dumps(res_body),
    }
