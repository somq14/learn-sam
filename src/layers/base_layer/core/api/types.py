from typing import Any, Callable, Dict, List, Optional, TypedDict


class Context:
    """
    https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html
    """

    pass


class Event(TypedDict):
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
    body: Optional[str]
    isBase64Encoded: bool


class Response(TypedDict, total=False):
    """
    https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#apigateway-multivalue-headers-and-parameters
    """

    isBase64Encoded: bool
    statusCode: int
    headers: Dict[str, str]
    multiValueHeaders: Dict[str, List[str]]
    body: str


Handler = Callable[[Event, Context], Response]

HandlerDecorator = Callable[[Handler], Handler]
