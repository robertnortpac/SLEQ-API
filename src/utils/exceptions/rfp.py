from utils.exceptions.base import AppExceptionBase

class RfpNotFound(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Rfp not found
        """
        status_code = 404
        super().__init__(status_code=status_code, context=context)

class RfpAlreadyExists(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Rfp already exists
        """
        status_code = 409
        super().__init__(status_code=status_code, context=context)