class AppException(Exception):
    pass


class UserNotFoundError(AppException):
    pass


class UserAlreadyExistsError(AppException):
    pass


class InvalidCredentialsError(AppException):
    pass


class InvalidTokenError(AppException):
    pass


class SessionNotFoundError(AppException):
    pass


class InvalidSessionError(AppException):
    pass


class ForbiddenError(AppException):
    pass


class ValidationError(AppException):
    pass