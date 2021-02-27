import typing


class ApiError(Exception):
    statusCode: int
    errorCode: str
    errorMessage: str
    errorDetail: typing.Optional[typing.Any]
    internalDetail: typing.Optional[typing.Any]

    def __init__(
        self,
        statusCode: int,
        errorCode: str,
        errorMessage: str,
        errorDetail: typing.Optional[typing.Any] = None,
        internalDetail: typing.Optional[typing.Any] = None,
    ) -> None:
        self.statusCode = statusCode
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.errorDetail = errorDetail
        self.internalDetail = internalDetail
