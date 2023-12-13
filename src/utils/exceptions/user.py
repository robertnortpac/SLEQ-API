from utils.exceptions.base import AppExceptionBase

class UserNotFound(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        User not found
        """
        status_code = 404
        super().__init__(status_code=status_code, context=context)

class UserAlreadyExists(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        User already exists
        """
        status_code = 409
        super().__init__(status_code=status_code, context=context)