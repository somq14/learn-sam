import json
from typing import Any, Dict, Optional

import cerberus  # type: ignore

from .error import ApiError


def decode_request_body(body: Optional[str], schema: Dict[str, Any]) -> Any:
    if body is None:
        raise ApiError(400, "ERR000", "request body must not be empty")  # TODO: CODE

    try:
        body = json.loads(body)
    except json.JSONDecodeError as e:
        raise ApiError(
            400, "ERR000", "request body must be a json", None, e
        )  # TODO: CODE

    validator = cerberus.Validator(schema)
    validated_body = validator.validated(body)
    if validated_body is None:
        raise ApiError(
            400,
            "ERR000",
            "request body is invalid",
            validator.errors,
            internalDetail={"body": body, "schema": schema, "errors": validator.errors},
        )  # TODO: CODE

    return validated_body


def decode_request_parameter(parameter: Dict[str, str], schema: Dict[str, Any]) -> Any:
    return ""
    # if body is None:
    #     raise core.api.ApiError(
    #         400, "ERR000", "request body must not be empty"
    #     )  # TODO: CODE

    # try:
    #     body = json.loads(body)
    # except json.JSONDecodeError as e:
    #     raise core.api.ApiError(
    #         400, "ERR000", "request body must be a json", None, e
    #     )  # TODO: CODE

    # validator = cerberus.Validator(schema)
    # validated_body = validator.validated(body)
    # if validated_body is None:
    #     raise core.api.ApiError(
    #         400,
    #         "ERR000",
    #         "request body is invalid",
    #         validator.errors,
    #         internalDetail={"body": body, "schema": schema, "errors": validator.errors},
    #     )  # TODO: CODE

    # return validated_body
