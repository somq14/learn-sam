import datetime
import json
import os

import cerberus  # type: ignore
import core.decorator
import core.lambda_handler

from . import service

print(os.environ)


@core.decorator.handle_error()
@core.decorator.enable_cors(origin="http://localhost:3000")
def lambda_handler(
    event: core.lambda_handler.ApiGatewayLambdaEvent,
    context: core.lambda_handler.Context,
) -> core.lambda_handler.ApiGatewayLambdaResponse:
    # JSONのパース
    body = None
    try:
        if event["body"] is None:
            return {
                "statusCode": 400,
                "body": "no payload",
            }
        body = json.loads(event["body"])
    except json.JSONDecodeError as e:
        print(e)
        return {
            "statusCode": 400,
            "body": "payload is not a json",
        }

    # JSONのバリデーション
    validator = cerberus.Validator(
        {
            "userId": {"type": "string", "required": True},
            "password": {"type": "string", "required": True},
        }
    )
    if not validator.validate(body):
        return {
            "statusCode": 400,
            "body": "invalid json",
        }

    try:
        input: service.LoginServiceInput = {
            "user_id": body["userId"],
            "password": body["password"],
        }
        output = service.login_service(input)
    except Exception as e:
        print(e)
        pass

    return {
        "statusCode": 200,
        "headers": {
            "Set-Cookie": ";".join(
                [
                    "SessionId={}".format(output["session_id"]),
                    "Expires={}".format(
                        output["expires_at"]
                        .astimezone(datetime.timezone.utc)
                        .strftime("%a, %d %b %Y %H:%M:%S GMT")
                    ),
                    "Secure",
                    "HttpOnly",
                    # "SameSite=Strict",
                    # "Domain="
                ]
            )
        },
        "body": json.dumps({}),
    }
