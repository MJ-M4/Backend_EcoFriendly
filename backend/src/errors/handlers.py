"""
Flask error helpers — zero numeric literals!

• ApiError is our single custom exception class.
• `register_error_handlers(app)` attaches the handler once at app-startup.
"""
from http import HTTPStatus
from typing import Callable

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from src.errors import ErrorMessage


class ApiError(HTTPException):
    """Raise this anywhere in the codebase to return a JSON error payload."""

    def __init__(
        self,
        message: ErrorMessage,
        status: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(description=message)
        # werkzeug looks for .code; store the *numeric value* internally,
        # but we never write the number as a literal.
        self.code: int = int(status.value)
        self.message: str = str(message)


def register_error_handlers(app: Flask) -> None:  # noqa: D401  (simple func)
    """Attach handlers so all ApiError responses are uniform JSON."""

    @app.errorhandler(ApiError)
    def _api_error_handler(err: ApiError):  # noqa: D401
        resp = jsonify(error=err.message)
        resp.status_code = err.code
        return resp

    # Handle true "not-found" routes uniformly — still *textual* msg, no digits.
    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def _not_found(_):  # noqa: D401
        raise ApiError(ErrorMessage.BIN_NOT_FOUND, HTTPStatus.NOT_FOUND)

    # Optionally, convert any uncaught Exception → generic DB_ERROR
    @app.errorhandler(Exception)
    def _fallback(err):  # noqa: D401
        # Avoid leaking stack traces; log internally instead.
        app.logger.exception("Unhandled exception: %s", err)
        raise ApiError(ErrorMessage.DB_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR)
