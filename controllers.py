from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from services import (
    AuthService, MenuCategoryService, MenuService,
    OrderService, PaymentService, ReservationService,
    SalesReportService, InventoryService
)
from schemas import user_schema
from utils.response import success_response, error_response
from middleware import jwt_required_custom, admin_required
from validations import (
    validate_register_data, validate_login_data,
    validate_category_create, validate_category_update,
    validate_menu_create, validate_menu_update,
    validate_order_data, validate_payment_data,
    validate_reservation_data, validate_sales_report_data,
    validate_inventory_data
)

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
@api_bp.route("/auth/register", methods=["POST"])
def register():
    data, error = validate_register_data(request.get_json() or {})
    if error:
        return error

    user, error = AuthService.register_user(**data)
    if error:
        return error

    return success_response("User registered successfully",user_schema.dump(user),201)


@api_bp.route("/auth/login", methods=["POST"])
def login():
    data, error = validate_login_data(request.get_json() or {})
    if error:
        return error

    auth_data, error = AuthService.authenticate_user(**data)
    if error:
        return error

    auth_data["user"] = user_schema.dump(auth_data["user"])
    return success_response("Login successful", auth_data, 200)


@api_bp.route("/auth/me", methods=["GET"])
@jwt_required_custom
def get_me():
    user_id = int(get_jwt_identity())
    user, error = AuthService.get_user_by_id(user_id)
    if error:
        return error

    return success_response("User retrieved", user_schema.dump(user), 200)


@api_bp.route("/auth/change-password", methods=["PUT"])
@jwt_required_custom
def change_password():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    user, error = AuthService.update_password(
        user_id,
        data.get("old_password"),
        data.get("new_password")
    )
    if error:
        return error

    return success_response("Password updated", user_schema.dump(user), 200)


@api_bp.route("/auth/change-role/<int:user_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def change_role(user_id):
    if user_id == int(get_jwt_identity()):
        return error_response("You cannot change your own role", 403)

    user, error = AuthService.change_role(
        user_id,
        request.get_json().get("role")
    )
    if error:
        return error

    return success_response("Role updated", user_schema.dump(user), 200)


@api_bp.route("/categories", methods=["POST"])
@jwt_required_custom
@admin_required
def create_category():
    data, error = validate_category_create(request.get_json() or {})
    if error:
        return error

    category, error = MenuCategoryService.create_category(data)
    if error:
        return error

    return success_response("Category created", category, 201)


@api_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = MenuCategoryService.get_all_categories()
    return success_response("Categories retrieved", categories, 200)


@api_bp.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def update_category(category_id):
    data, error = validate_category_update(request.get_json() or {})
    if error:
        return error

    category, error = MenuCategoryService.update_category(category_id, data)
    if error:
        return error

    return success_response("Category updated", category, 200)


@api_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required_custom
@admin_required
def delete_category(category_id):
    category, error = MenuCategoryService.delete_category(category_id)
    if error:
        return error

    return success_response("Category deleted", category, 200)


@api_bp.route("/menu", methods=["POST"])
@jwt_required_custom
@admin_required
def create_menu():
    data, error = validate_menu_create(request.get_json() or {})
    if error:
        return error

    menu, error = MenuService.create_menu(data)
    if error:
        return error

    return success_response("Menu created", menu, 201)


@api_bp.route("/menu", methods=["GET"])
def get_all_menu():
    menus = MenuService.get_all_menus()
    return success_response("Menus retrieved", menus, 200)


@api_bp.route("/menu/<int:menu_id>", methods=["GET"])
def get_menu(menu_id):
    menu = MenuService.get_menu_by_id(menu_id)
    if not menu:
        return error_response("Menu not found", 404)

    return success_response("Menu retrieved", menu, 200)


@api_bp.route("/menu/<int:menu_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def update_menu(menu_id):
    data, error = validate_menu_update(request.get_json() or {})
    if error:
        return error

    menu, error = MenuService.update_menu(menu_id, data)
    if error:
        return error

    return success_response("Menu updated", menu, 200)


@api_bp.route("/menu/<int:menu_id>", methods=["DELETE"])
@jwt_required_custom
@admin_required
def delete_menu(menu_id):
    menu, error = MenuService.delete_menu(menu_id)
    if error:
        return error

    return success_response("Menu deleted", menu, 200)


@api_bp.route("/orders", methods=["POST"])
@jwt_required_custom
def create_order():
    data, error = validate_order_data(request.get_json() or {})
    if error:
        return error

    data["user_id"] = int(get_jwt_identity())

    order, error = OrderService.create_order(data)
    if error:
        return error

    return success_response("Order created", order, 201)


@api_bp.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required_custom
def get_order(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order:
        return error_response("Order not found", 404)

    return success_response("Order retrieved", order, 200)


@api_bp.route("/orders", methods=["GET"])
@jwt_required_custom
@admin_required
def get_all_orders():
    orders = OrderService.get_all_orders()
    return success_response("Orders retrieved", orders, 200)


@api_bp.route("/orders/<int:order_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def update_order(order_id):
    order, error = OrderService.update_order(order_id, request.get_json() or {})
    if error:
        return error

    return success_response("Order updated", order, 200)


@api_bp.route("/orders/<int:order_id>", methods=["DELETE"])
@jwt_required_custom
@admin_required
def delete_order(order_id):
    order, error = OrderService.delete_order(order_id)
    if error:
        return error

    return success_response("Order deleted", order, 200)


@api_bp.route("/payments", methods=["POST"])
@jwt_required_custom
def create_payment():
    data, error = validate_payment_data(request.get_json() or {})
    if error:
        return error

    data["user_id"] = int(get_jwt_identity())

    payment, error = PaymentService.create_payment(data)
    if error:
        return error

    return success_response("Payment created", payment, 201)


@api_bp.route("/payments", methods=["GET"])
@jwt_required_custom
@admin_required
def get_all_payments():
    payments = PaymentService.get_all_payments()
    return success_response("Payments retrieved", payments, 200)


@api_bp.route("/payments/<int:payment_id>", methods=["GET"])
@jwt_required_custom
def get_payment(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    if not payment:
        return error_response("Payment not found", 404)

    return success_response("Payment retrieved", payment, 200)


@api_bp.route("/payments/<int:payment_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def update_payment(payment_id):
    payment, error = PaymentService.update_payment(
        payment_id,
        request.get_json() or {}
    )
    if error:
        return error

    return success_response("Payment updated", payment, 200)


@api_bp.route("/payments/<int:payment_id>", methods=["DELETE"])
@jwt_required_custom
@admin_required
def delete_payment(payment_id):
    payment, error = PaymentService.delete_payment(payment_id)
    if error:
        return error

    return success_response("Payment deleted", payment, 200)


@api_bp.route("/reservations", methods=["POST"])
@jwt_required_custom
@admin_required
def create_reservation():
    data, error = validate_reservation_data(request.get_json() or {})
    if error:
        return error

    reservation, error = ReservationService.create_reservation(data)
    if error:
        return error

    return success_response("Reservation created", reservation, 201)


@api_bp.route("/reservations", methods=["GET"])
@jwt_required_custom
def get_reservations():
    reservations = ReservationService.get_all_reservations()
    return success_response("Reservations retrieved", reservations, 200)


@api_bp.route("/reservations/<int:reservation_id>", methods=["GET"])
@jwt_required_custom
def get_reservation(reservation_id):
    reservation = ReservationService.get_reservation_by_id(reservation_id)
    if not reservation:
        return error_response("Reservation not found", 404)

    return success_response("Reservation retrieved", reservation, 200)


@api_bp.route("/reservations/<int:reservation_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def update_reservation(reservation_id):
    reservation, error = ReservationService.update_reservation(
        reservation_id,
        request.get_json() or {}
    )
    if error:
        return error

    return success_response("Reservation updated", reservation, 200)


@api_bp.route("/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required_custom
@admin_required
def delete_reservation(reservation_id):
    reservation, error = ReservationService.delete_reservation(reservation_id)
    if error:
        return error

    return success_response("Reservation deleted", reservation, 200)


@api_bp.route("/sales-reports", methods=["POST"])
@jwt_required_custom
@admin_required
def create_sales_report():
    data, error = validate_sales_report_data(request.get_json() or {})
    if error:
        return error

    report, error = SalesReportService.create_report(data)
    if error:
        return error

    return success_response("Sales report created", report, 201)


@api_bp.route("/sales-reports", methods=["GET"])
@jwt_required_custom
@admin_required
def get_sales_reports():
    reports = SalesReportService.get_all_reports()
    return success_response("Sales reports retrieved", reports, 200)


@api_bp.route("/sales-reports/<int:report_id>", methods=["GET"])
@jwt_required_custom
@admin_required
def get_sales_report(report_id):
    report = SalesReportService.get_report_by_id(report_id)
    if not report:
        return error_response("Sales report not found", 404)

    return success_response("Sales report retrieved", report, 200)


@api_bp.route("/sales-reports/<int:report_id>", methods=["PUT"])
@jwt_required_custom
@admin_required
def update_sales_report(report_id):
    report, error = SalesReportService.update_report(
        report_id,
        request.get_json() or {}
    )
    if error:
        return error

    return success_response("Sales report updated", report, 200)


@api_bp.route("/sales-reports/<int:report_id>", methods=["DELETE"])
@jwt_required_custom
@admin_required
def delete_sales_report(report_id):
    report, error = SalesReportService.delete_report(report_id)
    if error:
        return error

    return success_response("Sales report deleted", report, 200)


@api_bp.route("/inventory", methods=["POST"])
@jwt_required_custom
@admin_required
def create_inventory_item():
    data, error = validate_inventory_data(request.get_json() or {})
    if error:
        return error

    item, error = InventoryService.create_item(data)
    if error:
        return error

    return success_response("Inventory item created", item, 201)


@api_bp.route("/inventory", methods=["GET"])
@jwt_required_custom
def get_inventory():
    items = InventoryService.get_all_items()
    return success_response("Inventory retrieved", items, 200)


@api_bp.route("/inventory/<int:item_id>", methods=["GET"])
@jwt_required_custom
def get_inventory_item(item_id):
    item = InventoryService.get_item_by_id(item_id)
    if not item:
        return error_response("Inventory item not found", 404)

    return success_response("Inventory item retrieved", item, 200)


@api_bp.route("/inventory/<int:item_id>/increase", methods=["PATCH"])
@jwt_required_custom
@admin_required
def increase_stock(item_id):
    data = request.get_json() or {}
    item, error = InventoryService.increase_stock(
        item_id,
        data.get("quantity"),
        data.get("note")
    )
    if error:
        return error

    return success_response("Stock increased", item, 200)


@api_bp.route("/inventory/<int:item_id>/decrease", methods=["PATCH"])
@jwt_required_custom
@admin_required
def decrease_stock(item_id):
    data = request.get_json() or {}
    item, error = InventoryService.decrease_stock(
        item_id,
        data.get("quantity"),
        data.get("note")
    )
    if error:
        return error

    return success_response("Stock decreased", item, 200)


@api_bp.route("/inventory/<int:item_id>/adjust", methods=["PATCH"])
@jwt_required_custom
@admin_required
def adjust_stock(item_id):
    data = request.get_json() or {}
    item, error = InventoryService.adjust_stock(
        item_id,
        data.get("quantity"),
        data.get("note")
    )
    if error:
        return error

    return success_response("Stock adjusted", item, 200)
