from app.utils.exceptions.base import AppExceptionBase

class SicNotFound(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Sic not found
        """
        status_code = 404
        super().__init__(status_code=status_code, context=context)

class SicAlreadyExists(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Sic already exists
        """
        status_code = 409
        super().__init__(status_code=status_code, context=context)