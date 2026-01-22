import os
from decimal import Decimal
from flask import Flask
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from database.db import db, init_db
from models import User, MenuCategory, MenuItem, Inventory, InventoryLog

load_dotenv()

app = Flask(__name__)

DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

if not DATABASE_URI:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

with app.app_context():
    try:
        admin = User.query.filter_by(email="johnzeru73@gmail.com").first()
        if not admin:
            admin = User(
                username="yohannes",
                email="johnzeru73@gmail.com",
                role="admin",
                is_active=True,
                password_hash=generate_password_hash(ADMIN_PASSWORD)
            )
            db.session.add(admin)
            print("Admin user created")
        else:
            print("ℹAdmin user already exists")

        categories_data = [
            ("Burgers", "Delicious gourmet burgers"),
            ("Pizzas", "Hand-tossed pizzas with fresh toppings"),
            ("Pastas", "Italian pasta dishes"),
            ("Drinks", "Soft drinks, juices, and cocktails"),
            ("Desserts", "Cakes, ice creams, and sweets"),
            ("Salads", "Fresh and healthy salads"),
            ("Breakfast", "Morning specials and coffee"),
            ("Seafood", "Fresh seafood dishes"),
            ("Vegan", "Plant-based options"),
            ("Snacks", "Quick bites and appetizers"),
            ("Ethiopian Main Dishes", "Traditional Ethiopian meals"),
            ("Ethiopian Breakfast", "Traditional Ethiopian breakfast items"),
            ("Ethiopian Drinks", "Traditional Ethiopian beverages"),
        ]

        category_map = {}
        for name, desc in categories_data:
            category = MenuCategory.query.filter_by(name=name).first()
            if not category:
                category = MenuCategory(name=name, description=desc)
                db.session.add(category)
            category_map[name] = category

        db.session.flush()

        menu_items_data = [
            ("Cheeseburger", "300.00", "Burgers"),
            ("Veggie Burger", "280.00", "Burgers"),
            ("Margherita Pizza", "450.00", "Pizzas"),
            ("Pepperoni Pizza", "500.00", "Pizzas"),
            ("Spaghetti Carbonara", "400.00", "Pastas"),
            ("Fettuccine Alfredo", "420.00", "Pastas"),
            ("Coke", "60.00", "Drinks"),
            ("Orange Juice", "80.00", "Drinks"),
            ("Chocolate Cake", "150.00", "Desserts"),
            ("Caesar Salad", "200.00", "Salads"),
            ("Pancakes", "180.00", "Breakfast"),
            ("Grilled Salmon", "800.00", "Seafood"),
            ("Vegan Burger", "300.00", "Vegan"),
            ("French Fries", "100.00", "Snacks"),
            ("Doro Wot", "600.00", "Ethiopian Main Dishes"),
            ("Kitfo", "550.00", "Ethiopian Main Dishes"),
            ("Tibs", "500.00", "Ethiopian Main Dishes"),
            ("Shiro Wot", "250.00", "Ethiopian Main Dishes"),
            ("Misir Wot", "230.00", "Ethiopian Main Dishes"),
            ("Gomen Besiga", "450.00", "Ethiopian Main Dishes"),
            ("Beyaynetu", "300.00", "Ethiopian Main Dishes"),
            ("Firfir", "180.00", "Ethiopian Breakfast"),
            ("Chechebsa", "170.00", "Ethiopian Breakfast"),
            ("Kinche", "150.00", "Ethiopian Breakfast"),
            ("Ethiopian Coffee", "50.00", "Ethiopian Drinks"),
            ("Tea (Shai)", "30.00", "Ethiopian Drinks"),
            ("Tella", "80.00", "Ethiopian Drinks"),
        ]

        for name, price, cat in menu_items_data:
            category = category_map[cat]
            exists = MenuItem.query.filter_by(name=name, category_id=category.id).first()
            if not exists:
                db.session.add(
                    MenuItem(
                        name=name,
                        price=Decimal(price),
                        category_id=category.id
                    )
                )

        inventory_data = [
            ("Beef Patty", 50, "pcs", 5, "Local Farm"),
            ("Burger Bun", 100, "pcs", 10, "Bakery Co."),
            ("Tomato", 200, "pcs", 20, "Fresh Farms"),
            ("Cheese Slice", 150, "pcs", 15, "Dairy Co."),
            ("Spaghetti", 100, "kg", 10, "Italian Foods"),
            ("Salmon Fillet", 50, "kg", 5, "Seafood Co."),
            ("Injera", 200, "pcs", 30, "Local Injera House"),
            ("Berbere Spice", 25, "kg", 5, "Spice Market"),
            ("Niter Kibbeh", 20, "kg", 3, "Local Dairy"),
            ("Chickpeas", 60, "kg", 10, "Grain Supplier"),
            ("Lentils", 50, "kg", 10, "Grain Supplier"),
            ("Beef Meat", 80, "kg", 15, "Local Butcher"),
            ("Chicken", 70, "kg", 10, "Poultry Farm"),
        ]

        for name, qty, unit, threshold, supplier in inventory_data:
            item = Inventory.query.filter_by(item_name=name).first()
            if not item:
                item = Inventory(
                    item_name=name,
                    stock_quantity=qty,
                    unit=unit,
                    threshold=threshold,
                    supplier=supplier
                )
                db.session.add(item)
                db.session.add(
                    InventoryLog(
                        inventory_item=item,
                        change_type="IN",
                        quantity_changed=qty,
                        note="Initial stock"
                    )
                )

        db.session.commit()
        print("Database seeded successfully")

    except Exception as e:
        db.session.rollback()
        print("Seeding failed:", e)
