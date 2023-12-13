from utils.exceptions.base import AppExceptionBase

class CompanyNotFound(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Company not found
        """
        status_code = 404
        super().__init__(status_code=status_code, context=context)

class CompanyAlreadyExists(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Company already exists
        """
        status_code = 409
        super().__init__(status_code=status_code, context=context)