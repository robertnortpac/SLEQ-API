from app.utils.exceptions.base import AppExceptionBase


class AuthenticationError(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Authentication error
        """
        status_code = 401
        super().__init__(status_code=status_code, context=context)

class PasswordsDontMatch(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Passwords don't match
        """
        status_code = 400
        super().__init__(status_code=status_code, context=context)

class InvalidClaimCode(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Invalid claim code
        """
        status_code = 400
        super().__init__(status_code=status_code, context=context)

class InvalidPassword(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Invalid password
        """
        status_code = 401
        super().__init__(status_code=status_code, context=context)

class InvalidOTP(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Invalid OTP
        """
        status_code = 401
        super().__init__(status_code=status_code, context=context)


class AccountAlreadyClaimed(AppExceptionBase):
    def __init__(self, context: dict = None):
        """
        Account already claimed
        """
        status_code = 400
        super().__init__(status_code=status_code, context=context)

