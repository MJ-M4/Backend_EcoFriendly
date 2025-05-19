# src/errors/auth_errors.py

class InvalidCredentialsError(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)
