from models import (
    User, MenuItem, MenuCategory, Order, OrderItem, Payment,
    Reservation, SalesReport, Inventory, InventoryLog
)
from database.db import db
from utils.response import success_response, error_response
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
from decimal import Decimal
import random, string
from sqlalchemy.exc import SQLAlchemyError


class AuthService:

    @staticmethod
    def register_user(username, email, password, role="user"):
        username = (username or "").strip()
        email = (email or "").strip()
        password = (password or "").strip()
        role = (role or "user").strip()

        if User.query.filter_by(email=email).first():
            return None, error_response("Email already exists", 400)

        if User.query.filter_by(username=username).first():
            return None, error_response("Username already exists", 400)

        new_user = User(username=username, email=email, role=role, is_active=True)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(f"Database error: {str(e)}", 500)

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None, error_response("Invalid credentials", 401)

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=12))
        return {"access_token": access_token, "user": user}, None

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, error_response("User not found", 404)
        return user, None

    @staticmethod
    def update_password(user_id, old_password, new_password):
        user = User.query.get(user_id)
        if not user:
            return None, error_response("User not found", 404)
        if not user.check_password(old_password):
            return None, error_response("Old password is incorrect", 400)

        user.set_password(new_password)
        try:
            db.session.commit()
            return user, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(f"Database error: {str(e)}", 500)

    @staticmethod
    def change_role(user_id, new_role):
        user = User.query.get(user_id)
        if not user:
            return None, error_response("User not found", 404)

        user.role = new_role
        try:
            db.session.commit()
            return user, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(f"Database error: {str(e)}", 500)

    @staticmethod
    def deactivate_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, error_response("User not found", 404)
        user.is_active = False
        try:
            db.session.commit()
            return user, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(f"Database error: {str(e)}", 500)

    @staticmethod
    def activate_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, error_response("User not found", 404)
        user.is_active = True
        try:
            db.session.commit()
            return user, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(f"Database error: {str(e)}", 500)

class MenuCategoryService:

    @staticmethod
    def _active_query():
        return MenuCategory.query.filter_by(is_deleted=False)

    @staticmethod
    def create_category(data):
        category = MenuCategory(
            name=data["name"].strip(),
            description=data.get("description"),
            is_active=data.get("is_active", True)
        )
        try:
            db.session.add(category)
            db.session.commit()
            return category, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_all_categories():
        return MenuCategoryService._active_query().all()

    @staticmethod
    def get_category_by_id(category_id):
        return MenuCategoryService._active_query().filter_by(id=category_id).first()

    @staticmethod
    def update_category(category_id, data):
        category = MenuCategoryService.get_category_by_id(category_id)
        if not category:
            return None, error_response("Category not found", 404)
        for key in ["name", "description", "is_active"]:
            if key in data:
                setattr(category, key, data[key])
        try:
            db.session.commit()
            return category, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def delete_category(category_id):
        category = MenuCategoryService.get_category_by_id(category_id)
        if not category:
            return None, error_response("Category not found", 404)
        category.is_deleted = True
        try:
            db.session.commit()
            return category, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)


class MenuService:

    @staticmethod
    def _active_query():
        return MenuItem.query.filter_by(is_deleted=False)

    @staticmethod
    def create_menu(data):
        category = MenuCategory.query.get(data["category_id"])
        if not category:
            return None, error_response("Category not found", 404)
        menu_item = MenuItem(
            name=data["name"].strip(),
            description=data.get("description"),
            price=Decimal(data["price"]),
            is_available=data.get("is_available", True),
            category_id=data["category_id"]
        )
        try:
            db.session.add(menu_item)
            db.session.commit()
            return menu_item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_menu_by_id(menu_id):
        return MenuService._active_query().filter_by(id=menu_id).first()

    @staticmethod
    def get_all_menus():
        return MenuService._active_query().all()

    @staticmethod
    def update_menu(menu_id, data):
        menu_item = MenuService.get_menu_by_id(menu_id)
        if not menu_item:
            return None, error_response("Menu item not found", 404)
        if "category_id" in data:
            category = MenuCategory.query.get(data["category_id"])
            if not category:
                return None, error_response("Category not found", 404)
        for key in ["name", "description", "price", "is_available", "category_id"]:
            if key in data:
                if key == "price":
                    setattr(menu_item, key, Decimal(data[key]))
                else:
                    setattr(menu_item, key, data[key])
        try:
            db.session.commit()
            return menu_item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def delete_menu(menu_id):
        menu_item = MenuService.get_menu_by_id(menu_id)
        if not menu_item:
            return None, error_response("Menu item not found", 404)
        menu_item.is_deleted = True
        try:
            db.session.commit()
            return menu_item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)


class OrderService:

    @staticmethod
    def _active_query():
        return Order.query

    @staticmethod
    def _generate_order_number(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def create_order(data):
        order = Order(
            user_id=data["user_id"],
            order_number=OrderService._generate_order_number(),
            status=data.get("status", "pending"),
            payment_status=data.get("payment_status", "unpaid"),
            payment_method=data.get("payment_method", "cash"),
            service_type=data.get("service_type", "dine_in"),
            notes=data.get("notes"),
            discount=float(data.get("discount", 0.0))
        )
        try:
            db.session.add(order)
            db.session.flush()
            for item_data in data.get("items", []):
                menu_item = MenuItem.query.get(item_data["menu_item_id"])
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=int(item_data.get("quantity", 1)),
                    price=float(item_data.get("price", menu_item.price))
                )
                db.session.add(order_item)
            db.session.flush()
            order.calculate_totals()
            db.session.commit()
            return order, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def update_order(order_id, data):
        order = Order.query.get(order_id)
        if not order:
            return None, error_response("Order not found", 404)
        for key in ["status", "payment_status", "payment_method", "service_type", "notes", "discount"]:
            if key in data:
                setattr(order, key, data[key])
        if "items" in data:
            order.items.clear()
            db.session.flush()
            for item_data in data["items"]:
                menu_item = MenuItem.query.get(item_data["menu_item_id"])
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=int(item_data.get("quantity", 1)),
                    price=float(item_data.get("price", menu_item.price))
                )
                db.session.add(order_item)
        try:
            db.session.flush()
            order.calculate_totals()
            db.session.commit()
            return order, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return None, error_response("Order not found", 404)
        try:
            db.session.delete(order)
            db.session.commit()
            return order, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

class PaymentService:

    @staticmethod
    def _active_query():
        return Payment.query

    @staticmethod
    def create_payment(data):
        payment = Payment(
            order_id=data["order_id"],
            user_id=data["user_id"],
            amount=float(data.get("amount")),
            payment_method=data.get("payment_method", "cash"),
            status=data.get("status", "unpaid")
        )
        try:
            db.session.add(payment)
            order = Order.query.get(payment.order_id)
            order.payment_status = payment.status
            db.session.commit()
            return payment, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_payment_by_id(payment_id):
        return Payment.query.get(payment_id)

    @staticmethod
    def get_all_payments():
        return Payment.query.all()

    @staticmethod
    def update_payment(payment_id, data):
        payment = Payment.query.get(payment_id)
        if not payment:
            return None, error_response("Payment not found", 404)
        for key in ["order_id", "user_id", "amount", "payment_method", "status"]:
            if key in data:
                setattr(payment, key, data[key])
        try:
            db.session.commit()
            return payment, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def delete_payment(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return None, error_response("Payment not found", 404)
        try:
            db.session.delete(payment)
            db.session.commit()
            return payment, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

class ReservationService:

    @staticmethod
    def _active_query():
        return Reservation.query

    @staticmethod
    def create_reservation(data):
        reservation = Reservation(**data)
        try:
            db.session.add(reservation)
            db.session.commit()
            return reservation, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_reservation_by_id(reservation_id):
        return Reservation.query.get(reservation_id)

    @staticmethod
    def get_all_reservations():
        return Reservation.query.all()

    @staticmethod
    def update_reservation(reservation_id, data):
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return None, error_response("Reservation not found", 404)
        for key, value in data.items():
            setattr(reservation, key, value)
        try:
            db.session.commit()
            return reservation, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def delete_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return None, error_response("Reservation not found", 404)
        try:
            db.session.delete(reservation)
            db.session.commit()
            return reservation, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)


class SalesReportService:

    @staticmethod
    def _active_query():
        return SalesReport.query

    @staticmethod
    def create_report(data):
        report = SalesReport(**data)
        try:
            db.session.add(report)
            db.session.commit()
            return report, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_report_by_id(report_id):
        return SalesReport.query.get(report_id)

    @staticmethod
    def get_all_reports():
        return SalesReport.query.all()

    @staticmethod
    def update_report(report_id, data):
        report = SalesReport.query.get(report_id)
        if not report:
            return None, error_response("Sales report not found", 404)
        for key, value in data.items():
            setattr(report, key, value)
        try:
            db.session.commit()
            return report, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def delete_report(report_id):
        report = SalesReport.query.get(report_id)
        if not report:
            return None, error_response("Sales report not found", 404)
        try:
            db.session.delete(report)
            db.session.commit()
            return report, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)


class InventoryService:

    @staticmethod
    def _active_query():
        return Inventory.query

    @staticmethod
    def create_item(data):
        item = Inventory(**data)
        try:
            db.session.add(item)
            db.session.commit()
            return item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def get_item_by_id(item_id):
        return Inventory.query.get(item_id)

    @staticmethod
    def get_all_items():
        return Inventory.query.all()

    @staticmethod
    def increase_stock(item_id, quantity, note=None):
        if quantity <= 0:
            return None, error_response("Quantity must be greater than 0", 400)
        item = Inventory.query.get(item_id)
        if not item:
            return None, error_response("Inventory item not found", 404)
        item.stock_quantity += quantity
        item.last_restock_date = datetime.utcnow()
        log = InventoryLog(
            inventory_id=item.id,
            change_type="IN",
            quantity_changed=quantity,
            note=note
        )
        try:
            db.session.add(log)
            db.session.commit()
            return item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def decrease_stock(item_id, quantity, note=None):
        if quantity <= 0:
            return None, error_response("Quantity must be greater than 0", 400)
        item = Inventory.query.get(item_id)
        if not item:
            return None, error_response("Inventory item not found", 404)
        if item.stock_quantity < quantity:
            return None, error_response("Insufficient stock", 400)
        item.stock_quantity -= quantity
        log = InventoryLog(
            inventory_id=item.id,
            change_type="OUT",
            quantity_changed=-quantity,
            note=note
        )
        try:
            db.session.add(log)
            db.session.commit()
            return item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def adjust_stock(item_id, quantity, note=None):
        if quantity == 0:
            return None, error_response("Adjustment quantity cannot be zero", 400)
        item = Inventory.query.get(item_id)
        if not item:
            return None, error_response("Inventory item not found", 404)
        new_stock = item.stock_quantity + quantity
        if new_stock < 0:
            return None, error_response("Stock cannot go negative", 400)
        item.stock_quantity = new_stock
        log = InventoryLog(
            inventory_id=item.id,
            change_type="ADJUSTMENT",
            quantity_changed=quantity,
            note=note
        )
        try:
            db.session.add(log)
            db.session.commit()
            return item, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, error_response(str(e), 500)

    @staticmethod
    def low_stock_items():
        items = Inventory.query.filter(Inventory.stock_quantity <= Inventory.threshold).all()
        return items
