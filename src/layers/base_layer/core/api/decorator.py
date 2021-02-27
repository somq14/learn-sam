import json

import core.api


def _enable_cors(
    origin: str,
) -> core.api.HandlerDecorator:
    def decorator(
        lambda_handler: core.api.Handler,
    ) -> core.api.Handler:
        def wrapped_func(
            event: core.api.Event,
            context: core.api.Context,
        ) -> core.api.Response:
            response = lambda_handler(event, context)
            if "headers" not in response:
                response["headers"] = {}
            if "Allow-Access-Control-Allow-Origin" not in response["headers"]:
                response["headers"]["Access-Control-Allow-Origin"] = origin
            return response

        return wrapped_func

    return decorator


def _handle_error() -> core.api.HandlerDecorator:
    def decorator(
        lambda_handler: core.api.Handler,
    ) -> core.api.Handler:
        def wrapped_func(
            event: core.api.Event,
            context: core.api.Context,
        ) -> core.api.Response:
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


def default_interceptor() -> core.api.HandlerDecorator:
    def decorator(
        lambda_handler: core.api.Handler,
    ) -> core.api.Handler:
        @_enable_cors(origin="http://localhost:3000")
        @_handle_error()
        def wrapped_func(
            event: core.api.Event,
            context: core.api.Context,
        ) -> core.api.Response:
            return lambda_handler(event, context)

        return wrapped_func

    return decorator
