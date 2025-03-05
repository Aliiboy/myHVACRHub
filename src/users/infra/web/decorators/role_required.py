from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from typing import Any

from flask import Response
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from common.infra.web.dtos.generic import ErrorResponse


def role_required(
    *allowed_roles: str,
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    """Décorateur pour vérifier si l'utilisateur est autorisé à accéder à une ressource

    Args:
        *allowed_roles (str): Rôles autorisés

    Returns:
        Callable[[Callable[..., Response]], Callable[..., Response]]: Décorateur pour vérifier si l'utilisateur est autorisé à accéder à une ressource
    """

    def decorator(fn: Callable[..., Response]) -> Callable[..., Response]:
        """Décorateur pour vérifier si l'utilisateur est autorisé à accéder à une ressource

        Args:
            fn (Callable[..., Response]): Fonction à décorer

        Returns:
            Callable[..., Response]: Réponse de succès ou d'erreur
        """

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            """Wrapper pour vérifier si l'utilisateur est autorisé à accéder à une ressource

            Returns:
                Response: Réponse de succès ou d'erreur
            """
            verify_jwt_in_request()
            claims = get_jwt()
            user_role: str | None = claims.get("role")
            if user_role not in allowed_roles:
                return ErrorResponse(
                    code=HTTPStatus.FORBIDDEN,
                    message="Accès interdit : niveau insuffisant.",
                ).to_response()
            return fn(*args, **kwargs)

        return wrapper

    return decorator
