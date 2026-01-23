from database.db import ma
from decimal import Decimal
from models import (
    User,
    MenuCategory,
    MenuItem,
    Order,
    OrderItem,
    Payment,
    Reservation,
    SalesReport,
    Inventory,
    InventoryLog,
)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    is_active = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)


class MenuCategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = MenuCategory
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    description = ma.auto_field()
    is_active = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


class MenuItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MenuItem
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    description = ma.auto_field()
    price = ma.Method("get_price", "set_price")
    is_available = ma.auto_field()
    category_id = ma.auto_field(required=True)
    created_at = ma.auto_field(dump_only=True)

    def get_price(self, obj):
        return float(obj.price)

    def set_price(self, value):
        return Decimal(value)



class OrderItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrderItem
        load_instance = True

    id = ma.auto_field(dump_only=True)
    menu_item_id = ma.auto_field(required=True)
    quantity = ma.auto_field()
    price = ma.Method("get_price", "set_price")
    line_total = ma.Method("get_line_total", dump_only=True)

    def get_price(self, obj):
        return float(obj.price)

    def set_price(self, value):
        return Decimal(value)

    def get_line_total(self, obj):
        return float(obj.line_total())



class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = ma.auto_field(dump_only=True)
    order_number = ma.auto_field(dump_only=True)
    status = ma.auto_field()
    payment_status = ma.auto_field()
    subtotal = ma.Method("get_subtotal", dump_only=True)
    total_price = ma.Method("get_total", dump_only=True)
    created_at = ma.auto_field(dump_only=True)

    def get_subtotal(self, obj):
        return float(obj.subtotal)

    def get_total(self, obj):
        return float(obj.total_price)




class PaymentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Payment
        load_instance = True

    id = ma.auto_field(dump_only=True)
    order_id = ma.auto_field(required=True)
    user_id = ma.auto_field(required=True)
    amount = ma.Method("get_amount", "set_amount")
    payment_method = ma.auto_field()
    status = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)

    def get_amount(self, obj):
        return float(obj.amount)

    def set_amount(self, value):
        return Decimal(value)


class ReservationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reservation
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(required=True)
    table_number = ma.auto_field()
    reservation_time = ma.auto_field()
    status = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)



class SalesReportSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SalesReport
        load_instance = True

    id = ma.auto_field(dump_only=True)
    report_date = ma.auto_field()
    total_sales = ma.Method("get_total_sales")
    total_orders = ma.auto_field()
    total_items_sold = ma.auto_field()
    generated_by = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)

    def get_total_sales(self, obj):
        return float(obj.total_sales)



class InventorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True

    id = ma.auto_field(dump_only=True)
    item_name = ma.auto_field()
    stock_quantity = ma.auto_field()
    unit = ma.auto_field()
    threshold = ma.auto_field()
    supplier = ma.auto_field()
    last_restock_date = ma.auto_field(dump_only=True)


class InventoryLogSchema(ma.SQLAlchemySchema):
    class Meta:
        model = InventoryLog
        load_instance = True

    id = ma.auto_field(dump_only=True)
    inventory_id = ma.auto_field()
    change_type = ma.auto_field()
    quantity_changed = ma.auto_field()
    note = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

category_schema = MenuCategorySchema()
categories_schema = MenuCategorySchema(many=True)

menu_item_schema = MenuItemSchema()
menu_items_schema = MenuItemSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

sales_report_schema = SalesReportSchema()
sales_reports_schema = SalesReportSchema(many=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

inventory_log_schema = InventoryLogSchema()
inventory_logs_schema = InventoryLogSchema(many=True)
