from utils.response import error_response
from decimal import Decimal, InvalidOperation
from datetime import date, datetime
import re

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

ORDER_STATUS = ["pending", "processing", "completed", "cancelled"]
PAYMENT_STATUS = ["unpaid", "paid", "failed", "refunded"]
SERVICE_TYPES = ["dine_in", "take_away", "delivery"]
PAYMENT_METHODS = ["cash", "card", "mobile"]
RESERVATION_STATUS = ["pending", "confirmed", "cancelled"]

def _add_error(errors, field, message):
    if field not in errors:
        errors[field] = message


def _validate_string(value, field, errors, required=False, max_length=None):
    if value is None:
        if required:
            _add_error(errors, field, f"{field.replace('_',' ').title()} is required")
        return

    value = str(value).strip()
    if not value:
        _add_error(errors, field, f"{field.replace('_',' ').title()} cannot be empty")
        return

    if max_length and len(value) > max_length:
        _add_error(errors, field, f"{field.replace('_',' ').title()} must not exceed {max_length} characters")


def _validate_integer(value, field, errors, required=False, min_value=None):
    if value is None:
        if required:
            _add_error(errors, field, f"{field.replace('_',' ').title()} is required")
        return

    try:
        value = int(value)
        if min_value is not None and value < min_value:
            _add_error(errors, field, f"{field.replace('_',' ').title()} must be >= {min_value}")
    except (ValueError, TypeError):
        _add_error(errors, field, f"{field.replace('_',' ').title()} must be an integer")


def _validate_boolean(value, field, errors):
    if value is not None and not isinstance(value, bool):
        _add_error(errors, field, f"{field.replace('_',' ').title()} must be true or false")


def _validate_price(value, field, errors, required=False):
    if value is None:
        if required:
            _add_error(errors, field, f"{field.replace('_',' ').title()} is required")
        return

    try:
        price = Decimal(value)
        if price < 0:
            _add_error(errors, field, f"{field.replace('_',' ').title()} must be >= 0")
    except (InvalidOperation, TypeError):
        _add_error(errors, field, f"{field.replace('_',' ').title()} must be a valid number")


def validate_register_data(data):
    errors = {}

    _validate_string(data.get("username"), "username", errors, required=True, max_length=50)
    _validate_string(data.get("email"), "email", errors, required=True)
    _validate_string(data.get("password"), "password", errors, required=True, max_length=100)

    if "email" in data and not re.match(EMAIL_REGEX, str(data["email"])):
        _add_error(errors, "email", "Invalid email format")

    if "password" in data and len(str(data["password"])) < 6:
        _add_error(errors, "password", "Password must be at least 6 characters")

    if errors:
        return None, error_response("Validation error", errors, 400)

    return {
        "username": data["username"].strip(),
        "email": data["email"].strip(),
        "password": data["password"]
    }, None


def validate_login_data(data):
    errors = {}

    _validate_string(data.get("email"), "email", errors, required=True)
    _validate_string(data.get("password"), "password", errors, required=True)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return {
        "email": data["email"].strip(),
        "password": data["password"]
    }, None

def validate_category_create(data):
    errors = {}

    _validate_string(data.get("name"), "name", errors, required=True, max_length=100)
    _validate_string(data.get("description"), "description", errors, max_length=250)
    _validate_boolean(data.get("is_active"), "is_active", errors)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None


def validate_category_update(data):
    errors = {}

    if "name" in data:
        _validate_string(data.get("name"), "name", errors, max_length=100)

    if "description" in data:
        _validate_string(data.get("description"), "description", errors, max_length=250)

    if "is_active" in data:
        _validate_boolean(data.get("is_active"), "is_active", errors)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None

def validate_menu_create(data):
    errors = {}

    _validate_string(data.get("name"), "name", errors, required=True, max_length=100)
    _validate_string(data.get("description"), "description", errors, max_length=250)
    _validate_price(data.get("price"), "price", errors, required=True)
    _validate_integer(data.get("category_id"), "category_id", errors, required=True, min_value=1)
    _validate_boolean(data.get("is_available"), "is_available", errors)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None


def validate_menu_update(data):
    errors = {}

    if "name" in data:
        _validate_string(data.get("name"), "name", errors, max_length=100)

    if "description" in data:
        _validate_string(data.get("description"), "description", errors, max_length=250)

    if "price" in data:
        _validate_price(data.get("price"), "price", errors)

    if "category_id" in data:
        _validate_integer(data.get("category_id"), "category_id", errors, min_value=1)

    if "is_available" in data:
        _validate_boolean(data.get("is_available"), "is_available", errors)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None


def validate_order_data(data):
    errors = {}

    _validate_integer(data.get("user_id"), "user_id", errors, required=True, min_value=1)

    if not isinstance(data.get("items"), list) or not data.get("items"):
        _add_error(errors, "items", "Items must be a non-empty list")

    if "status" in data and data["status"] not in ORDER_STATUS:
        _add_error(errors, "status", f"Status must be one of {ORDER_STATUS}")

    if "payment_status" in data and data["payment_status"] not in PAYMENT_STATUS:
        _add_error(errors, "payment_status", f"Payment status must be one of {PAYMENT_STATUS}")

    if "service_type" in data and data["service_type"] not in SERVICE_TYPES:
        _add_error(errors, "service_type", f"Service type must be one of {SERVICE_TYPES}")

    if "discount" in data:
        try:
            if float(data["discount"]) < 0:
                _add_error(errors, "discount", "Discount must be >= 0")
        except (ValueError, TypeError):
            _add_error(errors, "discount", "Discount must be a number")

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None

def validate_payment_data(data):
    errors = {}

    _validate_integer(data.get("order_id"), "order_id", errors, required=True, min_value=1)
    _validate_integer(data.get("user_id"), "user_id", errors, required=True, min_value=1)

    if "status" in data and data["status"] not in PAYMENT_STATUS:
        _add_error(errors, "status", f"Status must be one of {PAYMENT_STATUS}")

    if "payment_method" in data and data["payment_method"] not in PAYMENT_METHODS:
        _add_error(errors, "payment_method", f"Payment method must be one of {PAYMENT_METHODS}")

    if "amount" in data:
        _validate_price(data.get("amount"), "amount", errors)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None

def validate_reservation_data(data):
    errors = {}

    _validate_integer(data.get("user_id"), "user_id", errors, required=True, min_value=1)
    _validate_integer(data.get("table_number"), "table_number", errors, required=True, min_value=1)

    if "reservation_time" not in data:
        _add_error(errors, "reservation_time", "Reservation time is required")
    else:
        try:
            reservation_time = datetime.fromisoformat(data["reservation_time"])
            if reservation_time < datetime.utcnow():
                _add_error(errors, "reservation_time", "Reservation time cannot be in the past")
        except (ValueError, TypeError):
            _add_error(errors, "reservation_time", "Invalid datetime format")

    if "status" in data and data["status"] not in RESERVATION_STATUS:
        _add_error(errors, "status", f"Status must be one of {RESERVATION_STATUS}")

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None


def validate_sales_report_data(data):
    errors = {}

    if "report_date" not in data:
        _add_error(errors, "report_date", "Report date is required")
    else:
        try:
            report_date = date.fromisoformat(data["report_date"])
            if report_date > date.today():
                _add_error(errors, "report_date", "Report date cannot be in the future")
        except (ValueError, TypeError):
            _add_error(errors, "report_date", "Invalid date format")

    if "generated_by" in data:
        _validate_integer(data.get("generated_by"), "generated_by", errors, min_value=1)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None

def validate_inventory_data(data):
    errors = {}

    _validate_string(data.get("item_name"), "item_name", errors, required=True, max_length=100)
    _validate_integer(data.get("stock_quantity"), "stock_quantity", errors, min_value=0)
    _validate_integer(data.get("threshold"), "threshold", errors, min_value=0)
    _validate_string(data.get("unit"), "unit", errors)
    _validate_string(data.get("supplier"), "supplier", errors)

    if errors:
        return None, error_response("Validation error", errors, 400)

    return data, None
