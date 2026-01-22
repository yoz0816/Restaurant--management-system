[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Vn0I8K1_)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21503176&assignment_repo_type=AssignmentRepo)
# SE_python_project202 

A backend Restaurant Ordering & Management System

 <h1>Project Overview</h1>

The Restaurant Management backend system that digitizes restaurant operations. It enables customers to browse meals and place orders, while admins can manage menu items, track orders, and handle table reservations.

   Why This Project?
Eliminates manual ordering and billing
Reduces human errors
Provides real-time management
Helps restaurants digitize workflow
Useful for learning Flask + MySQL

  <h1>Who Can Use It?</h1>
Restaurants & cafés
Small food businesses
Students learning backend development
Developers building ordering systems


 <b>Key Features</b>

 Customer Features
- View all menu items
- Add/remove items 
- Place orders with auto total
- Reserve tables 

Admin Features
- Secure admin login
- Add/edit/delete menu items
- View/manage customer orders
- Approve table reservations

System Architecture
- Backend: Flask (Python)
- Database: MySQL
- ORM: SQLAlchemy (optiona)
<h1>API Documentation</h1>

this is complete API list including request and response examples. it is just sample

<u><b>Auth API Documentation (Postman Style)</b></u>

Base URL  /api/auth

<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the Auth controller is working.
- Headers: None
- Body: None
- Response:
```python
{
  "message": "Auth controller is working!",
  "data": { "status": "ok" },
  "status": 200
}
```

<u>2. Register User</u>
- POST /register
- Description: Create a new user.
- Headers: 
   - Content-Type: application/json

``` python 
Body (JSON):
{
  "username": "john_doe",
  "email": "john@gmail.com",
  "password": "securePassword123"
}


Success Response (201):
{
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@gmail.com",
    "role": "user",
    "is_active": true
  },
  "status": 201
}

Error Responses:
400 Username, email, or password missing / Email or username exists
```

<u>3. Login</u>
- POST /login
- Description: Authenticate user and return JWT token.
- Headers:
     -  Content-Type: application/json
```python
Body (JSON):
{
  "email": "john@gmail.com",
  "password": "securePassword123"
}


Success Response (200):
{
  "message": "Login successful",
  "data": {
    "access_token": "JWT_TOKEN_HERE",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@gmail.com",
      "role": "user",
      "is_active": true
    }
  },
  "status": 200
}


Error Responses:
400 Email or password missing
```
<u>1. Get Current User</u>
- GET /me
- Description: Get details of logged-in user.
- Headers: 
    - Authorization: Bearer JWT_TOKEN_HERE
```python
Response (200):
{
  "message": "User retrieved successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@gmail.com",
    "role": "user",
    "is_active": true
  },
  "status": 200
}


Error Responses:
401 Missing or invalid token
404 User not found 
```

<u>5. Change Password</u>
- PUT /change-password
- Description: Change the password for the logged-in user.
- Headers: 
     - Authorization: Bearer JWT_TOKEN_HERE
     - Content-Type: application/json

```python
Body (JSON):
{
  "old_password": "oldPass123",
  "new_password": "newSecurePass456"
}

Success Response (200):
{
  "message": "Password updated successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@gmail.com",
    "role": "user",
    "is_active": true
  },
  "status": 200
}


Error Responses:
400 Old/new password missing / Old password incorrect
```

<u>6. Change User Role (Admin Only)</u>
- PUT /change-role/:user_id
- Description: Update the role of a user (admin only).
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json

```python
Body (JSON):
{
  "role": "admin"
}


Success Response (200):
{
  "message": "Role updated successfully",
  "data": {
    "id": 2,
    "username": "jane_doe",
    "email": "jane@gmail.com",
    "role": "admin",
    "is_active": true
  },
  "status": 200
}


Error Responses:
400 Role missing
404 User not found
401 Unauthorized if not admin
```

<u>7. Deactivate User (Admin Only)</u>
- PUT /deactivate/:user_id
- Description: Deactivate a user account.
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE

```python
Response (200):
{
  "message": "User deactivated successfully",
  "data": {
    "id": 2,
    "username": "jane_doe",
    "email": "jane@gmail.com",
    "role": "user",
    "is_active": false
  },
  "status": 200
}


Error Responses:
404 User not found
401 Unauthorized if not admin
```

<u>1. Activate User (Admin Only)</u>
- PUT /activate/:user_id
- Description: Activate a user account.
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE

```python
Response (200):
{
  "message": "User activated successfully",
  "data": {
    "id": 2,
    "username": "jane_doe",
    "email": "jane@gmail.com",
    "role": "user",
    "is_active": true
  },
  "status": 200
}


Error Responses:
404 User not found
401 Unauthorized if not admin
```

<u>9. Check Admin Users</u>
- GET /check-admins
- Description: List all admin users.
- Headers: None
```python
Response (200):
{
  "admin_count": 2,
  "admins": [
    {"id": 1, "username": "admin1", "email": "admin1@gmail.com"},
    {"id": 3, "username": "admin2", "email": "admin2@gmail.com"}
  ]
}
```
<u><b>Category API Documentation (Postman Style)</u></b>

<b>Base URL: /api/categories</b>

<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the Category controller is working.
- Headers: None
- Body: None
```python
Response:

{
  "message": "Category controller working!",
  "data": { "status": "ok" },
  "status": 200
}
```
<u>2. Create Category</u>
- POST /
- Description: Create a new menu category (Admin only).
- Headers:
   - Authorization: Bearer JWT_TOKEN_HERE
   - Content-Type: application/json
```python
Body (JSON):

{
  "name": "Fast Food",
  "description": "Quick meals and snacks"
}


Success Response (201):

{
  "message": "Category created successfully",
  "data": {
    "id": 1,
    "name": "Fast Food",
    "description": "Quick meals and snacks",
    "created_at": "2025-12-20T08:00:00",
    "updated_at": "2025-12-20T08:00:00"
  },
  "status": 201
}


Error Responses: 400 Missing required fields (name)
```

<u>3. Get All Categories</u>
- GET /
- Description: Retrieve all categories (only active ones, not soft-deleted).
- Headers: None
- Body: None
```python
Success Response (200):

{
  "message": "Categories retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Fast Food",
      "description": "Quick meals and snacks",
      "created_at": "2025-12-20T08:00:00",
      "updated_at": "2025-12-20T08:00:00",
      "menu_items": []
    }
  ],
  "status": 200
}
```
<u>4. Get Category By ID</u>
- GET /<int:category_id>
- Description: Get details of a specific category by ID.
- Headers: None
- Body: None
```python
Success Response (200):

{
  "message": "Category retrieved successfully",
  "data": {
    "id": 1,
    "name": "Fast Food",
    "description": "Quick meals and snacks",
    "created_at": "2025-12-20T08:00:00",
    "updated_at": "2025-12-20T08:00:00",
    "menu_items": []
  },
  "status": 200
}


Error Responses: 404 Category not found
```

<u>5. Update Category</u>
- PUT /<int:category_id>
- Description: Update an existing category (Admin only).
- Headers:
   -  Authorization: Bearer JWT_TOKEN_HERE
   -  Content-Type: application/json
```python
Body (JSON):

{
  "name": "Premium Fast Food",
  "description": "Upgraded quick meals"
}


Success Response (200):

{
  "message": "Category updated successfully",
  "data": {
    "id": 1,
    "name": "Premium Fast Food",
    "description": "Upgraded quick meals",
    "created_at": "2025-12-20T08:00:00",
    "updated_at": "2025-12-20T08:15:00",
    "menu_items": []
  },
  "status": 200
}


Error Responses:
- 404 Category not found
- 400 Validation error (empty name)
```

<u>6. Delete Category (Soft Delete)</u>
- DELETE /<int:category_id>
- Description: Soft delete a category (Admin only).
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
```python
Success Response (200):

{
  "message": "Category deleted successfully",
  "status": 200
}


Error Responses:
- 404 Category not found
- 500 Database error<u>
```
<u><b>Menu API Documentation</u></b>

<b>Base URL: /api/menu</b>
<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the Menu controller is working.
- Headers: None
- Body: None
```python
Response (200):

{
  "message": "Menu controller working!",
  "data": { "status": "ok" },
  "status": 200
}
```
<u>2. Create Menu Item</u>
- POST /
- Description: Create a new menu item. Admin only.
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json
```python
Body (JSON):

{
  "name": "Cheese Burger",
  "description": "Beef burger with cheese",
  "price": 12.5,
  "is_available": true,
  "category_id": 1
}


Success Response (201):

{
  "message": "Menu item created successfully",
  "data": {
    "id": 1,
    "name": "Cheese Burger",
    "description": "Beef burger with cheese",
    "price": 12.50,
    "is_available": true,
    "category": {
      "id": 1,
      "name": "Fast Food"
    },
    "category_id": 1,
    "created_at": "2025-12-20T10:00:00",
    "updated_at": "2025-12-20T10:00:00"
  },
  "status": 201
}


Error Responses:
- 400 Missing fields or invalid price
- 404 Category does not exist
```
<u>3. Get Menu Item by ID</u>
- GET /<menu_id>
- Description: Retrieve a menu item by its ID.
- Headers: None
- Body: None
```python
Success Response (200):

{
  "message": "Menu item retrieved successfully",
  "data": {
    "id": 1,
    "name": "Cheese Burger",
    "description": "Beef burger with cheese",
    "price": 12.50,
    "is_available": true,
    "category": {
      "id": 1,
      "name": "Fast Food"
    },
    "category_id": 1,
    "created_at": "2025-12-20T10:00:00",
    "updated_at": "2025-12-20T10:00:00"
  },
  "status": 200
}


Error Response:
- 404 Menu item not found
```
<u>4. Get All Menu Items</u>
- GET /
- Description: Retrieve all menu items (non-deleted).
- Headers: None
- Body: None
```python
Success Response (200):

{
  "message": "Menu items retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Cheese Burger",
      "description": "Beef burger with cheese",
      "price": 12.50,
      "is_available": true,
      "category": { "id": 1, "name": "Fast Food" },
      "category_id": 1,
      "created_at": "2025-12-20T10:00:00",
      "updated_at": "2025-12-20T10:00:00"
    },
    {
      "id": 2,
      "name": "Veggie Pizza",
      "description": "Pizza with vegetables",
      "price": 15.00,
      "is_available": true,
      "category": { "id": 2, "name": "Special Menu" },
      "category_id": 2,
      "created_at": "2025-12-20T10:05:00",
      "updated_at": "2025-12-20T10:05:00"
    }
  ],
  "status": 200
}
```
<u>5. Update Menu Item</u>
- PUT /<menu_id>
- Description: Update a menu item. Admin only.
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json
```python
Body (JSON): (Any of the fields can be updated)

{
  "name": "Cheese Burger Deluxe",
  "price": 13.50,
  "is_available": false,
  "category_id": 1
}


Success Response (200):

{
  "message": "Menu item updated successfully",
  "data": {
    "id": 1,
    "name": "Cheese Burger Deluxe",
    "description": "Beef burger with cheese",
    "price": 13.50,
    "is_available": false,
    "category": { "id": 1, "name": "Fast Food" },
    "category_id": 1,
    "created_at": "2025-12-20T10:00:00",
    "updated_at": "2025-12-20T10:15:00"
  },
  "status": 200
}


Error Responses:
- 400 Invalid price
- 404 Menu item not found or category does not exist
```
<u>6. Delete Menu Item</u>
- DELETE /<menu_id>
- Description: Soft-delete a menu item. Admin only.
- Headers:
     - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Menu item deleted successfully",
  "status": 200
}


Error Response:
- 404 Menu item not found
```
<u><b>Orders API Documentation (Postman Style)</u></b>

<b>Base URL: /api/order</b>

<u>1. Test Endpoint</u>
-  GET /test
- Description: Check if the Order controller is working.
- Headers: None
- Body: None
```python
Response (200):

{
  "message": "Order controller working!",
  "data": { "status": "ok" },
  "status": 200
}
```

<u>2. Create Order</u>
- POST /
- Description: Create a new order (Authenticated users only).
- Headers:
     - Authorization: Bearer JWT_TOKEN_HERE
     - Content-Type: application/json
```python
Body (JSON):

{
  "user_id": 1,
  "items": [
    {"menu_item_id": 1, "quantity": 2, "price": 12.5},
    {"menu_item_id": 3, "quantity": 1}
  ],
  "status": "pending",
  "payment_status": "unpaid",
  "payment_method": "cash",
  "service_type": "dine_in",
  "notes": "Extra napkins, please",
  "discount": 5.0
}

Success Response (201):

{
  "message": "Order created successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "order_number": "AB12CD34",
    "status": "pending",
    "payment_status": "unpaid",
    "payment_method": "cash",
    "service_type": "dine_in",
    "notes": "Extra napkins, please",
    "subtotal": 40.0,
    "discount": 5.0,
    "total_price": 35.0,
    "items": [
      {
        "id": 1,
        "order_id": 1,
        "menu_item_id": 1,
        "quantity": 2,
        "price": 12.5,
        "line_total": 25.0,
        "menu_item": {
          "id": 1,
          "name": "Cheese Burger",
          "price": 12.5
        }
      }
    ],
    "created_at": "2025-12-20T12:00:00",
    "updated_at": "2025-12-20T12:00:00"
  },
  "status": 201
}

Error Responses:
- 400 Validation errors (missing user_id, items, invalid quantity or price)
- 404 User or Menu item does not exist

```
<u>3. Get Single Order</u>
- GET /<order_id>
- Description: Retrieve a specific order by ID (Authenticated users only).
- Headers: 
   - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Order retrieved successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "order_number": "AB12CD34",
    "status": "pending",
    "payment_status": "unpaid",
    "payment_method": "cash",
    "service_type": "dine_in",
    "notes": "Extra napkins, please",
    "subtotal": 40.0,
    "discount": 5.0,
    "total_price": 35.0,
    "items": [...],
    "created_at": "2025-12-20T12:00:00",
    "updated_at": "2025-12-20T12:00:00"
  },
  "status": 200
}

Error Response:
- 404 Order not found
```

<u>4. Get All Orders</u>
- GET /
- Description: Retrieve all orders (Admin only).
- Headers: 
     - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Orders retrieved successfully",
  "data": [
    {...}, {...}
  ],
  "status": 200
}
```

<u>5. Update Order</u>
- PUT /<order_id>
- Description: Update an existing order (Admin only).
- Headers:
     - Authorization: Bearer JWT_TOKEN_HERE
     - Content-Type: application/json
```python
Body (JSON): (Any of the fields can be updated)

{
  "status": "processing",
  "payment_status": "paid",
  "discount": 3.0,
  "items": [
    {"menu_item_id": 2, "quantity": 1, "price": 12.0}
  ]
}

Success Response (200):

{
  "message": "Order updated successfully",
  "data": {...},
  "status": 200
}

Error Responses:
- 400 Validation errors (invalid status, payment_status, quantity, or price)
- 404 Order not found

```
<u>6. Delete Order</u>
-DELETE /<order_id>
- Description: Delete an order (Admin only).
- Headers:
  - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Order deleted successfully",
  "status": 200
}

Error Responses:
- 404 Order not found
- 500 Database error
```
<u><b>Payments API Documentation (Postman Style)</b></u>

<b>Base URL: /api/payment</b>

<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the Payment controller is working.
- Headers: None
- Body: None
```python
Response (200):

{
  "message": "Payment controller working!",
  "data": { "status": "ok" },
  "status": 200
}
```
<u>2. Create Payment</u>
- POST /
- Description: Create a new payment (Authenticated users only).
- Headers:
     - Authorization: Bearer JWT_TOKEN_HERE
     - Content-Type: application/json
```python
Body (JSON):

{
  "order_id": 1,
  "user_id": 1,
  "amount": 35.0,
  "payment_method": "cash",
  "status": "paid"
}


Success Response (201):

{
  "message": "Payment created successfully",
  "data": {
    "id": 1,
    "order_id": 1,
    "user_id": 1,
    "amount": 35.0,
    "payment_method": "cash",
    "status": "paid",
    "created_at": "2025-12-20T12:00:00",
    "updated_at": "2025-12-20T12:00:00",
    "order": {...},
    "user": {...}
  },
  "status": 201
}


Error Responses:
- 400 Validation errors (missing fields, invalid status, or amount < 0)
- 404 Order or User does not exist
```
<u>3. Get Single Payment</u>
- GET /<payment_id>
- Description: Retrieve a specific payment by ID (Authenticated users only).
- Headers: 
     - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Payment retrieved successfully",
  "data": {
    "id": 1,
    "order_id": 1,
    "user_id": 1,
    "amount": 35.0,
    "payment_method": "cash",
    "status": "paid",
    "created_at": "2025-12-20T12:00:00",
    "updated_at": "2025-12-20T12:00:00",
    "order": {...},
    "user": {...}
  },
  "status": 200
}


Error Response:
- 404 Payment not found
```
<u>4. Get All Payments</u>
- GET /
- Description: Retrieve all payments (Admin only).
- Headers: 
     - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Payments retrieved successfully",
  "data": [
    {...}, {...}
  ],
  "status": 200
}
```
<u>5. Update Payment</u>
- PUT /<payment_id>
- Description: Update an existing payment (Admin only).
- Headers:
   - Authorization: Bearer JWT_TOKEN_HERE
   - Content-Type: application/json
```python
Body (JSON): (Any field can be updated)

{
  "amount": 40.0,
  "payment_method": "card",
  "status": "paid"
}


Success Response (200):

{
  "message": "Payment updated successfully",
  "data": {...},
  "status": 200
}


Error Responses:

- 400 Validation errors (invalid status, payment_method, or negative amount)
- 404 Payment not found
```
<u>6. Delete Payment</u>
- DELETE /<payment_id>
- Description: Delete a payment (Admin only).
- Headers: 
     - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Payment deleted successfully",
  "status": 200
}


Error Responses:
-404 Payment not found
```
<u><b>Inventory API Documentation (Postman Style)</b></u>

<b>Base URL: /api/inventory</b>

<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the Inventory controller is working.
- Headers: None
- Body: None
```python
Response:

{
  "message": "Inventory controller working!",
  "data": { "status": "ok" },
  "status": 200
}
```
<u>2. Create Inventory Item</u>
- POST /
- Description: Create a new inventory item (Admin only).
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json
```python
Body (JSON):

{
  "item_name": "Tomatoes",
  "stock_quantity": 50,
  "unit": "kg",
  "threshold": 10,
  "supplier": "Local Farm"
}

Success Response (201):

{
  "message": "Inventory item created successfully",
  "data": {
    "id": 1,
    "item_name": "Tomatoes",
    "stock_quantity": 50,
    "unit": "kg",
    "threshold": 10,
    "supplier": "Local Farm",
    "last_restock_date": null,
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T09:00:00",
    "logs": []
  },
  "status": 201
}

Error Responses:
- 400 Validation error (missing required fields or invalid values)
```

<u>3. Get All Inventory Items</u>
- GET /
- Description: Retrieve all inventory items.
- Headers: None
- Body: None
```python
Success Response (200):

{
  "message": "Inventory items retrieved successfully",
  "data": [
    {
      "id": 1,
      "item_name": "Tomatoes",
      "stock_quantity": 50,
      "unit": "kg",
      "threshold": 10,
      "supplier": "Local Farm",
      "last_restock_date": null,
      "created_at": "2025-12-21T09:00:00",
      "updated_at": "2025-12-21T09:00:00",
      "logs": []
    }
  ],
  "status": 200
}
```

<u>4. Get Inventory Item By ID</u>
- GET /int:item_id
- Description: Get details of a specific inventory item by ID.
- Headers: None
- Body: None
```python
Success Response (200):

{
  "message": "Inventory item retrieved successfully",
  "data": {
    "id": 1,
    "item_name": "Tomatoes",
    "stock_quantity": 50,
    "unit": "kg",
    "threshold": 10,
    "supplier": "Local Farm",
    "last_restock_date": null,
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T09:00:00",
    "logs": []
  },
  "status": 200
}

Error Responses:
- 404 Inventory item not found
```

<u>5. Increase Stock</u>
- PATCH /int:item_id
/increase
- Description: Increase stock quantity for an item (Admin only).
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json
```python
Body (JSON):

{
  "quantity": 20,
  "note": "Restocked from supplier"
}

Success Response (200):

{
  "message": "Stock increased successfully",
  "data": {
    "id": 1,
    "item_name": "Tomatoes",
    "stock_quantity": 70,
    "unit": "kg",
    "threshold": 10,
    "supplier": "Local Farm",
    "last_restock_date": "2025-12-21T10:00:00",
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T10:00:00",
    "logs": [
      {
        "id": 1,
        "inventory_id": 1,
        "change_type": "IN",
        "quantity_changed": 20,
        "note": "Restocked from supplier",
        "created_at": "2025-12-21T10:00:00"
      }
    ]
  },
  "status": 200
}

Error Responses:
- 400 Quantity must be greater than 0
- 404 Inventory item not found
```

<u>6. Decrease Stock</u>
- PATCH /int:item_id
/decrease
- Description: Decrease stock quantity for an item (Admin only).
- Headers: 
   - Authorization: Bearer JWT_TOKEN_HERE
  - Content-Type: application/json
```python
Body (JSON):

{
  "quantity": 15,
  "note": "Used in kitchen"
}

Success Response (200):

{
  "message": "Stock decreased successfully",
  "data": {
    "id": 1,
    "item_name": "Tomatoes",
    "stock_quantity": 55,
    "unit": "kg",
    "threshold": 10,
    "supplier": "Local Farm",
    "last_restock_date": "2025-12-21T10:00:00",
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T10:15:00",
    "logs": [
      {
        "id": 2,
        "inventory_id": 1,
        "change_type": "OUT",
        "quantity_changed": -15,
        "note": "Used in kitchen",
        "created_at": "2025-12-21T10:15:00"
      }
    ]
  },
  "status": 200
}

Error Responses:
- 400 Quantity must be greater than 0 / Insufficient stock
- 404 Inventory item not found
```

<u>7. Adjust Stock</u>
- PATCH /int:item_id
/adjust
- Description: Adjust stock quantity manually (Admin only).
- Headers: 
   - Authorization: Bearer JWT_TOKEN_HERE
  - Content-Type: application/json
```python
Body (JSON):

{
  "quantity": -5,
  "note": "Inventory correction"
}

Success Response (200):

{
  "message": "Stock adjusted successfully",
  "data": {
    "id": 1,
    "item_name": "Tomatoes",
    "stock_quantity": 50,
    "unit": "kg",
    "threshold": 10,
    "supplier": "Local Farm",
    "last_restock_date": "2025-12-21T10:00:00",
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T10:30:00",
    "logs": [
      {
        "id": 3,
        "inventory_id": 1,
        "change_type": "ADJUSTMENT",
        "quantity_changed": -5,
        "note": "Inventory correction",
        "created_at": "2025-12-21T10:30:00"
      }
    ]
  },
  "status": 200
}

Error Responses:
- 400 Adjustment quantity cannot be zero / Stock cannot go negative
- 404 Inventory item not found
```

<u>8. Get Low Stock Items</u>
- GET /low-stock
- Description: Retrieve all items where stock quantity ≤ threshold.
- Headers: 
 -  Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Low stock items retrieved successfully",
  "data": [
    {
      "id": 1,
      "item_name": "Tomatoes",
      "stock_quantity": 5,
      "unit": "kg",
      "threshold": 10,
      "supplier": "Local Farm",
      "last_restock_date": "2025-12-21T10:00:00",
      "created_at": "2025-12-21T09:00:00",
      "updated_at": "2025-12-21T10:30:00",
      "logs": []
    }
  ],
  "status": 200
}
```
<u><b>Reservation API Documentation (Postman Style)</b></u>

<b>Base URL: /api/reservations</b>

<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the Reservation controller is working.
- Headers: None
- Body: None
```python
Response:
{
  "message": "Reservation controller working!",
  "data": { "status": "ok" },
  "status": 200
}
```

<u>2. Create Reservation</u>
- POST /
- Description: Create a new reservation (Admin only).
- Headers:
   - Authorization: Bearer JWT_TOKEN_HERE
   - Content-Type: application/json
```python
Body (JSON):
{
  "user_id": 1,
  "table_number": 5,
  "reservation_time": "2025-12-25T18:30:00",
  "status": "pending"
}

Success Response (201):
{
  "message": "Reservation created successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "table_number": 5,
    "reservation_time": "2025-12-25T18:30:00",
    "status": "pending",
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T09:00:00",
    "user": { "id": 1, "name": "John Doe", ... }
  },
  "status": 201
}

Error Responses:
- 400 Validation error (missing or invalid fields)
```

<u>3. Get All Reservations</u>
- GET /
- Description: Retrieve all reservations.
- Headers: None
- Body: None
```python
Success Response (200):
{
  "message": "Reservations retrieved successfully",
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "table_number": 5,
      "reservation_time": "2025-12-25T18:30:00",
      "status": "pending",
      "created_at": "2025-12-21T09:00:00",
      "updated_at": "2025-12-21T09:00:00",
      "user": { "id": 1, "name": "John Doe", ... }
    }
  ],
  "status": 200
}
```

<u>4. Get Reservation By ID</u>
- GET /int:reservation_id
- Description: Get details of a specific reservation by ID.
- Headers: None
- Body: None
```python
Success Response (200):
{
  "message": "Reservation retrieved successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "table_number": 5,
    "reservation_time": "2025-12-25T18:30:00",
    "status": "pending",
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T09:00:00",
    "user": { "id": 1, "name": "John Doe", ... }
  },
  "status": 200
}

Error Responses:
- 404 Reservation not found
```

<u>5. Update Reservation</u>
- PUT /int:reservation_id
- Description: Update a reservation (Admin only).
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json
```python
Body (JSON):
{
  "table_number": 6,
  "reservation_time": "2025-12-25T19:00:00",
  "status": "confirmed"
}

Success Response (200):
{
  "message": "Reservation updated successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "table_number": 6,
    "reservation_time": "2025-12-25T19:00:00",
    "status": "confirmed",
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T10:00:00",
    "user": { "id": 1, "name": "John Doe", ... }
  },
  "status": 200
}

Error Responses:
- 400 Validation error (invalid fields)
- 404 Reservation not found
```

<u>6. Delete Reservation</u>
- DELETE /int:reservation_id
- Description: Delete a reservation (Admin only).
- Headers:
   - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):
{
  "message": "Reservation deleted successfully",
  "data": {},
  "status": 200
}

Error Responses:
- 404 Reservation not found
```
<u><b>SalesReport API Documentation (Postman Style)</b></u>

<b>Base URL: /api/sales-reports</b>

<u>1. Test Endpoint</u>
- GET /test
- Description: Check if the SalesReport controller is working.
- Headers: None
- Body: None
```python
Response:

{
  "message": "SalesReport controller working!",
  "data": { "status": "ok" },
  "status": 200
}


<u>2. Create Sales Report</u>
- POST /
- Description: Create a new sales report (Admin only).
- Headers:
    - Authorization: Bearer JWT_TOKEN_HERE
    - Content-Type: application/json
```python
Body (JSON):

{
  "report_date": "2025-12-21",
  "generated_by": 1
}

Success Response (201):

{
  "message": "Sales report created successfully",
  "data": {
    "id": 1,
    "report_date": "2025-12-21",
    "total_sales": 0.0,
    "total_orders": 0,
    "total_items_sold": 0,
    "generated_by": 1,
    "user": { "id": 1, "name": "Admin User", "email": "admin@gmail.com" },
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T09:00:00"
  },
  "status": 201
}

Error Responses:
- 400 Validation error (missing/invalid report_date or generated_by)
```

<u>3. Get All Sales Reports</u>
- GET /
- Description: Retrieve all sales reports.
- Headers:
    -  Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Sales reports retrieved successfully",
  "data": [
    {
      "id": 1,
      "report_date": "2025-12-21",
      "total_sales": 0.0,
      "total_orders": 0,
      "total_items_sold": 0,
      "generated_by": 1,
      "user": { "id": 1, "name": "Admin User", "email": "admin@gmail.com" },
      "created_at": "2025-12-21T09:00:00",
      "updated_at": "2025-12-21T09:00:00"
    }
  ],
  "status": 200
}
```

<u>4. Get Sales Report by ID</u>
- GET /int:report_id
- Description: Get details of a specific sales report by ID.
- Headers:
  - Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Sales report retrieved successfully",
  "data": {
    "id": 1,
    "report_date": "2025-12-21",
    "total_sales": 0.0,
    "total_orders": 0,
    "total_items_sold": 0,
    "generated_by": 1,
    "user": { "id": 1, "name": "Admin User", "email": "admin@gmail.com" },
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T09:00:00"
  },
  "status": 200
}

Error Responses:
- 404 Sales report not found
```

<u>5. Update Sales Report</u>
- PUT /int:report_id
- Description: Update a sales report (Admin only).
- Headers:
   - Authorization: Bearer JWT_TOKEN_HERE
   - Content-Type: application/json
```python
Body (JSON):

{
  "report_date": "2025-12-21",
  "generated_by": 2
}

Success Response (200):

{
  "message": "Sales report updated successfully",
  "data": {
    "id": 1,
    "report_date": "2025-12-21",
    "total_sales": 0.0,
    "total_orders": 0,
    "total_items_sold": 0,
    "generated_by": 2,
    "user": { "id": 2, "name": "Another Admin", "email": "admin2@gmail.com" },
    "created_at": "2025-12-21T09:00:00",
    "updated_at": "2025-12-21T10:00:00"
  },
  "status": 200
}

Error Responses:
- 400 Validation error
- 404 Sales report not found
```

<u>6. Delete Sales Report</u>
- DELETE /int:report_id
- Description: Delete a sales report (Admin only).
- Headers:
   -  Authorization: Bearer JWT_TOKEN_HERE
- Body: None
```python
Success Response (200):

{
  "message": "Sales report deleted successfully",
  "data": null,
  "status": 200
}

Error Responses:
- 404 Sales report not found
```
<u><b> Database Tables</u></b>
- users
- menu_categories
- menu_items
- orders
- order_items
- reservations
- inventory
- payments
- sales_reports
  

<u><b>How to Run This Project</b></u>
1. Install dependencies

2. Set up the MySQL database:
   - Open MySQL Workbench
   - Create a database (example: restaurant_db)
   - Import the SQL file if provided

3. Start the Flask app:
   python app.py

4. Open in browser:
   http://127.0.0.1:5000


