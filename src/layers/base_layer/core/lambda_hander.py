import typing
from typing import Dict


class LambdaContext(typing.TypedDict):
    pass


class ApiGatewayLambdaEvent(typing.TypedDict):
    body: str


class ApiGatewayLambdaResponse(typing.TypedDict):
    statusCode: int
    body: str
    headers: Dict[str, str]


ApiGatewayLambdaHandler = typing.Callable[
    [ApiGatewayLambdaEvent, LambdaContext], ApiGatewayLambdaResponse
]
