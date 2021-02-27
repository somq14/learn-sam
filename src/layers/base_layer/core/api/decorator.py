import json
import trace
import traceback

from .error import ApiError
from .types import Context, Event, Handler, HandlerDecorator, Response


def _enable_cors(
    origin: str,
) -> HandlerDecorator:
    def decorator(
        lambda_handler: Handler,
    ) -> Handler:
        def wrapped_func(
            event: Event,
            context: Context,
        ) -> Response:
            response = lambda_handler(event, context)
            if "headers" not in response:
                response["headers"] = {}
            if "Allow-Access-Control-Allow-Origin" not in response["headers"]:
                response["headers"]["Access-Control-Allow-Origin"] = origin
            return response

        return wrapped_func

    return decorator


def _handle_error() -> HandlerDecorator:
    def decorator(
        lambda_handler: Handler,
    ) -> Handler:
        def wrapped_func(
            event: Event,
            context: Context,
        ) -> Response:
            try:
                return lambda_handler(event, context)
            except ApiError as e:
                print(traceback.format_exc())  # TODO:
                errorResponse = {
                    "errorCode": e.errorCode,
                    "errorMessage": e.errorMessage,
                }
                if e.errorDetail is not None:
                    errorResponse["errorDetail"] = e.errorDetail

                return {
                    "statusCode": e.statusCode,
                    "body": json.dumps(errorResponse),
                }
            except BaseException:
                print(traceback.format_exc())  # TODO:
                return {
                    "statusCode": 500,
                    "body": json.dumps(
                        {
                            "errorCode": "500",
                            "errorMessage": "internal server error",
                        }  # TODO:
                    ),
                }

        return wrapped_func

    return decorator


def default_interceptor(access_control_allow_origin: str) -> HandlerDecorator:
    def decorator(
        lambda_handler: Handler,
    ) -> Handler:
        @_enable_cors(origin=access_control_allow_origin)
        @_handle_error()
        def wrapped_func(
            event: Event,
            context: Context,
        ) -> Response:
            return lambda_handler(event, context)

        return wrapped_func

    return decorator
