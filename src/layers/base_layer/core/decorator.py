import json

import core.lambda_handler
from core.lambda_handler import LambdaHandlerDecorator


def enable_cors(
    origin: str,
) -> LambdaHandlerDecorator:
    def decorator(
        lambda_handler: core.lambda_handler.ApiGatewayLambdaHandler,
    ) -> core.lambda_handler.ApiGatewayLambdaHandler:
        def wrapped_func(
            event: core.lambda_handler.ApiGatewayLambdaEvent,
            context: core.lambda_handler.Context,
        ) -> core.lambda_handler.ApiGatewayLambdaResponse:
            response = lambda_handler(event, context)
            if "headers" not in response:
                response["headers"] = {}
            if "Allow-Access-Control-Allow-Origin" not in response["headers"]:
                response["headers"]["Access-Control-Allow-Origin"] = origin
            return response

        return wrapped_func

    return decorator


def handle_error() -> LambdaHandlerDecorator:
    def decorator(
        lambda_handler: core.lambda_handler.ApiGatewayLambdaHandler,
    ) -> core.lambda_handler.ApiGatewayLambdaHandler:
        def wrapped_func(
            event: core.lambda_handler.ApiGatewayLambdaEvent,
            context: core.lambda_handler.Context,
        ) -> core.lambda_handler.ApiGatewayLambdaResponse:
            try:
                return lambda_handler(event, context)
            except BaseException as e:
                print(e)  # logging
                return {
                    "statusCode": 500,
                    "headers": {},
                    "body": json.dumps({"message": "Internal Server Error"}),
                }

        return wrapped_func

    return decorator
