CREATE DATABASE IF NOT EXISTS restaurant_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE restaurant_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(250),
    price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_menuitem_category
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_menuitem_name_category UNIQUE (name, category_id),
    CONSTRAINT check_menuitem_price_positive CHECK (price >= 0)
);

CREATE INDEX idx_menu_items_category_id ON menu_items(category_id);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('pending','processing','completed','cancelled') NOT NULL DEFAULT 'pending',
    payment_status ENUM('unpaid','paid','failed','refunded') NOT NULL DEFAULT 'unpaid',
    payment_method VARCHAR(50) NOT NULL DEFAULT 'cash',
    service_type VARCHAR(20) NOT NULL DEFAULT 'dine_in',
    notes TEXT,
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    discount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    total_price DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT check_order_subtotal_positive CHECK (subtotal >= 0),
    CONSTRAINT check_order_discount_positive CHECK (discount >= 0),
    CONSTRAINT check_order_total_positive CHECK (total_price >= 0),
    CONSTRAINT check_discount_not_exceed_subtotal CHECK (discount <= subtotal)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_orderitems_order
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_orderitems_menu_item
        FOREIGN KEY (menu_item_id)
        REFERENCES menu_items(id)
        ON DELETE RESTRICT,

    CONSTRAINT check_orderitem_quantity_positive CHECK (quantity > 0),
    CONSTRAINT check_orderitem_price_positive CHECK (price >= 0)
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    table_number INT NOT NULL,
    reservation_time DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_reservations_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT check_reservation_table_positive CHECK (table_number > 0),
    CONSTRAINT check_reservation_status_valid
        CHECK (status IN ('pending','confirmed','cancelled'))
);

CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL UNIQUE,
    stock_quantity INT NOT NULL DEFAULT 0,
    unit VARCHAR(50) NOT NULL DEFAULT 'pcs',
    threshold INT NOT NULL DEFAULT 5,
    supplier VARCHAR(100),
    last_restock_date DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT check_inventory_stock_positive CHECK (stock_quantity >= 0),
    CONSTRAINT check_inventory_threshold_positive CHECK (threshold >= 0)
);

CREATE TABLE inventory_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inventory_id INT NOT NULL,
    change_type VARCHAR(20) NOT NULL,
    quantity_changed INT NOT NULL,
    note VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventorylogs_inventory
        FOREIGN KEY (inventory_id)
        REFERENCES inventory(id)
        ON DELETE CASCADE,

    CONSTRAINT check_inventorylog_change_type
        CHECK (change_type IN ('IN','OUT','ADJUSTMENT')),

    CONSTRAINT check_inventorylog_quantity_nonzero
        CHECK (quantity_changed <> 0)
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    status ENUM('unpaid','paid','failed','refunded') NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_payments_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT check_payment_amount_positive CHECK (amount >= 0)
);

CREATE TABLE sales_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_date DATETIME NOT NULL,
    total_sales DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    total_orders INT NOT NULL DEFAULT 0,
    total_items_sold INT NOT NULL DEFAULT 0,
    generated_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_salesreports_user
        FOREIGN KEY (generated_by)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT check_sales_total_sales_non_negative CHECK (total_sales >= 0),
    CONSTRAINT check_sales_total_orders_non_negative CHECK (total_orders >= 0),
    CONSTRAINT check_sales_total_items_non_negative CHECK (total_items_sold >= 0)
);
