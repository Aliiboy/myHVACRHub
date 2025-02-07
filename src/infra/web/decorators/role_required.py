from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from typing import Any

from flask import Response
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from infra.web.dtos.generic import ClientErrorResponse


def role_required(
    *allowed_roles: str,
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    def decorator(fn: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            verify_jwt_in_request()
            claims = get_jwt()
            user_role: str | None = claims.get("role")
            if user_role not in allowed_roles:
                return ClientErrorResponse(
                    code=HTTPStatus.FORBIDDEN,
                    message="Accès interdit : niveau insuffisant.",
                ).to_response()
            return fn(*args, **kwargs)

        return wrapper

    return decorator
