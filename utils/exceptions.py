class AppException(Exception):
    def __init__(self, message="An error occurred", status_code=400,details=None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    
class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized access"):
        super().__init__(message, 401)


class ForbiddenException(AppException):
    def __init__(self, message="Forbidden access"):
        super().__init__(message, 403)


