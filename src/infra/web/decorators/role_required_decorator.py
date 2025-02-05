# type: ignore
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role", None)

            if user_role not in allowed_roles:
                # TODO: personaliser erreur
                return jsonify({"message": "Accès interdit : rôle insuffisant"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
