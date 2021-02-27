import typing
from typing import Any, Dict, List


class Context:
    """
    https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html
    """

    pass


class ApiGatewayLambdaEvent(typing.TypedDict):
    """
    https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    """

    resource: str
    path: str
    httpMethod: str
    headers: Dict[str, str]
    multiValueHeaders: Dict[str, List[str]]
    queryStringParameters: Dict[str, str]
    multiValueQueryStringParameters: Dict[str, List[str]]
    pathParameters: Dict[str, str]
    stageVariables: Dict[str, str]
    requestContext: Dict[str, Any]
    body: str
    isBase64Encoded: bool


class ApiGatewayLambdaResponse(typing.TypedDict, total=False):
    """
    https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#apigateway-multivalue-headers-and-parameters
    """

    isBase64Encoded: bool
    statusCode: int
    headers: Dict[str, str]
    multiValueHeaders: Dict[str, List[str]]
    body: str


ApiGatewayLambdaHandler = typing.Callable[
    [ApiGatewayLambdaEvent, Context], ApiGatewayLambdaResponse
]

T = typing.TypeVar("T")
Decorator = typing.Callable[[T], T]
LambdaHandlerDecorator = Decorator[ApiGatewayLambdaHandler]
