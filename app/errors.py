class AppError(Exception):
    """Base application error."""


class NotFoundError(AppError):
    def __init__(self, entity: str, entity_id: int | str):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} {entity_id} not found")


class ConflictError(AppError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(message)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden"):
        self.message = message
        super().__init__(message)