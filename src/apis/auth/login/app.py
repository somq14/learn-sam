import json

import cerberus  # type: ignore
import core.lambda_hander


def lambda_handler(
    event: core.lambda_hander.ApiGatewayLambdaEvent,
    context: core.lambda_hander.LambdaContext,
) -> core.lambda_hander.ApiGatewayLambdaResponse:
    # decode parameter
    # decode pathparameter
    # decode body
    body = None
    try:
        if event["body"] is None:
            return {"statusCode": 500}
        body = json.loads(event["body"])
    except json.JSONDecodeError as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": {},
            "body": "",
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": {},
            "body": "",
        }

    schema = {
        "userId": {"type": "string", "required": True},
        "password": {"type": "string", "required": True},
    }

    validator = cerberus.Validator(schema)
    validatedBody = validator.validated()
    if validatedBody is None:
        return {
            "statusCode": 400,
            "headers": {},
            "body": "",
        }

    print(validatedBody)

    print(body)
    return {
        "statusCode": 200,
        "headers": {},
        "body": "hello",
    }
