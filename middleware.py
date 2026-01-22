from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from services import AuthService
from utils.response import error_response

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return error_response("Token missing or invalid", 401)
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return error_response("Authentication required", 401)

        user_id = int(get_jwt_identity())
        user, error = AuthService.get_user_by_id(user_id)

        if error or not user:
            return error_response("User not found", 404)

        if not user.is_active:
            return error_response("User disabled", 403)

        if user.role != "admin":
            return error_response("Admin access required", 403)

        return fn(*args, **kwargs)
    return wrapper
