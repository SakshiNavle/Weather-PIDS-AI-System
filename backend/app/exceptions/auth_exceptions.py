class AuthenticationException(Exception):
    """Base authentication exception."""
    pass


class InvalidCredentialsException(AuthenticationException):
    """Raised when username or password is invalid."""
    pass


class UserAlreadyExistsException(AuthenticationException):
    """Raised when username already exists."""
    pass


class EmailAlreadyExistsException(AuthenticationException):
    """Raised when email already exists."""
    pass


class InvalidTokenException(AuthenticationException):
    """Raised when JWT token is invalid."""
    pass


class InactiveUserException(AuthenticationException):
    """Raised when inactive user tries to login."""
    pass