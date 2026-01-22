from datetime import datetime
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, Float, Numeric, Enum, ForeignKey, CheckConstraint, event
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from database.db import db

ALLOWED_PAYMENT_STATUSES = ["unpaid", "paid", "failed", "refunded"]
ALLOWED_ORDER_STATUSES = ["pending", "processing", "completed", "cancelled"]
ALLOWED_RESERVATION_STATUSES = ["pending", "confirmed", "cancelled"]
ALLOWED_INVENTORY_CHANGE_TYPES = ["IN", "OUT", "ADJUSTMENT"]

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan", lazy="select")
    sales_reports = relationship("SalesReport", back_populates="user", lazy="dynamic")
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class MenuCategory(db.Model):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    menu_items = relationship("MenuItem", back_populates="category", cascade="all, delete-orphan", lazy="dynamic")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Category name cannot be empty")
        return value

    def __repr__(self):
        return f"<MenuCategory {self.name}>"

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    category = relationship("MenuCategory", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item", lazy="select")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_menuitem_price_positive"),
        db.UniqueConstraint("name", "category_id", name="uq_menuitem_name_category")
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value.strip():
            raise ValueError("Menu item name cannot be empty")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be >= 0")
        return value

    def __repr__(self):
        return f"<MenuItem {self.name}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_orderitem_quantity_positive"),
        CheckConstraint("price >= 0", name="check_orderitem_price_positive"),
    )

    def line_total(self):
        return self.quantity * self.price

    def __repr__(self):
        return f"<OrderItem {self.id} - Order {self.order_id}>"

class Order(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_number = Column(String(20), unique=True, nullable=False)
    status = Column(Enum(*ALLOWED_ORDER_STATUSES, name="order_status_enum"), default="pending", nullable=False)
    payment_status = Column(Enum(*ALLOWED_PAYMENT_STATUSES, name="payment_status_enum"), default="unpaid", nullable=False)
    payment_method = Column(String(50), default="cash", nullable=False)
    service_type = Column(String(20), default="dine_in", nullable=False)
    notes = Column(Text, nullable=True)
    subtotal = Column(Numeric(12,2), default=Decimal("0.00"), nullable=False)
    discount = Column(Numeric(12,2), default=Decimal("0.00"), nullable=False)
    total_price = Column(Numeric(12,2), default=Decimal("0.00"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="select")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan", lazy="select")
    user = relationship("User", back_populates="orders")

    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="check_order_subtotal_positive"),
        CheckConstraint("discount >= 0", name="check_order_discount_positive"),
        CheckConstraint("total_price >= 0", name="check_order_total_positive"),
        CheckConstraint("discount <= subtotal", name="check_discount_not_exceed_subtotal"),
    )

    def calculate_totals(self):
        self.subtotal = sum([item.line_total() for item in self.items]) or Decimal("0.00")
        self.total_price = max(self.subtotal - self.discount, Decimal("0.00"))

@event.listens_for(Order, "before_insert")
@event.listens_for(Order, "before_update")
def update_order_totals(mapper, connection, target):
    target.calculate_totals()

class Payment(db.Model):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(Enum(*ALLOWED_PAYMENT_STATUSES, name="payment_status_enum"), default="unpaid", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    order = relationship("Order", back_populates="payments")
    user = relationship("User", back_populates="payments")

    __table_args__ = (
        CheckConstraint("amount >= 0", name="check_payment_amount_positive"),
    )

    def __repr__(self):
        return f"<Payment {self.id} | Order {self.order_id} | Amount {self.amount}>"

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    reservation_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(*ALLOWED_RESERVATION_STATUSES, name="reservation_status_enum"), default="pending", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="reservations")

    __table_args__ = (
        CheckConstraint("table_number > 0", name="check_reservation_table_positive"),
    )

    @validates("table_number")
    def validate_table_number(self, key, value):
        if value <= 0:
            raise ValueError("table_number must be positive")
        return value

    @validates("reservation_time")
    def validate_reservation_time(self, key, value):
        if value < datetime.utcnow():
            raise ValueError("reservation_time cannot be in the past")
        return value

    @validates("status")
    def validate_status(self, key, value):
        if value not in ALLOWED_RESERVATION_STATUSES:
            raise ValueError(f"status must be one of {ALLOWED_RESERVATION_STATUSES}")
        return value

    def __repr__(self):
        return f"<Reservation {self.id} | Table {self.table_number} | User {self.user_id} | Status {self.status}>"


class SalesReport(db.Model):
    __tablename__ = "sales_reports"
    id = Column(Integer, primary_key=True)
    report_date = Column(DateTime(timezone=True), nullable=False)
    total_sales = Column(Numeric(12,2), nullable=False, default=Decimal("0.00"))
    total_orders = Column(Integer, nullable=False, default=0)
    total_items_sold = Column(Integer, nullable=False, default=0)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="sales_reports")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("total_sales >= 0", name="check_sales_total_sales_non_negative"),
        CheckConstraint("total_orders >= 0", name="check_sales_total_orders_non_negative"),
        CheckConstraint("total_items_sold >= 0", name="check_sales_total_items_non_negative"),
    )

    def __repr__(self):
        return f"<SalesReport {self.report_date} | {self.total_sales} ETB>"

class Inventory(db.Model):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    item_name = Column(String(100), nullable=False, unique=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(50), nullable=False, default="pcs")
    threshold = Column(Integer, nullable=False, default=5)
    supplier = Column(String(100), nullable=True)
    last_restock_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    logs = relationship("InventoryLog", back_populates="inventory_item", cascade="all, delete-orphan", lazy="select")

    __table_args__ = (
        CheckConstraint("stock_quantity >= 0", name="check_inventory_stock_positive"),
        CheckConstraint("threshold >= 0", name="check_inventory_threshold_positive"),
    )

    def __repr__(self):
        return f"<Inventory {self.item_name} | Stock {self.stock_quantity}>"

class InventoryLog(db.Model):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False)
    change_type = Column(Enum(*ALLOWED_INVENTORY_CHANGE_TYPES, name="inventory_change_type_enum"), nullable=False)
    quantity_changed = Column(Integer, nullable=False)
    note = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    inventory_item = relationship("Inventory", back_populates="logs")

    __table_args__ = (
        CheckConstraint("quantity_changed != 0", name="check_inventorylog_quantity_nonzero"),
    )

    @validates("change_type")
    def validate_change_type(self, key, value):
        if value not in ALLOWED_INVENTORY_CHANGE_TYPES:
            raise ValueError(f"change_type must be one of {ALLOWED_INVENTORY_CHANGE_TYPES}")
        return value

@event.listens_for(InventoryLog, "before_insert")
@event.listens_for(InventoryLog, "before_update")
def update_inventory_stock(mapper, connection, target):
    inv = target.inventory_item
    if target.change_type == "IN":
        inv.stock_quantity += target.quantity_changed
    elif target.change_type == "OUT":
        if inv.stock_quantity - target.quantity_changed < 0:
            raise ValueError(f"Not enough stock for {inv.item_name}")
        inv.stock_quantity -= target.quantity_changed
    elif target.change_type == "ADJUSTMENT":
        inv.stock_quantity = max(inv.stock_quantity + target.quantity_changed, 0)
    inv.last_restock_date = datetime.utcnow()
