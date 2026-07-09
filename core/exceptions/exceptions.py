class AppException(Exception):  # noqa: N818 — nazwa zgodna z wzorcem ARCHITEKTURA.md
    """Bazowy wyjątek aplikacji — mapowany globalnie na envelope błędu."""

    status_code: int = 500
    key_type_error: str = "Exception"

    def __init__(self, message: str, type_module: str, type_error: str = "exception"):
        super().__init__(message)
        self.message = message
        self.type_module = type_module  # nazwa funkcji, w której powstał błąd
        self.type_error = type_error


class NotFoundError(AppException):
    status_code = 404
    key_type_error = "NotFound"


class ConflictError(AppException):
    status_code = 409
    key_type_error = "IntegrityError"


class IntegrityViolationError(ConflictError):
    """Naruszenie constraintów DB (duplikat, FK)."""


class ExternalServiceError(AppException):
    status_code = 502


class DatabaseError(AppException):
    status_code = 500
