# Database Design — cardiac.exe

## 1. Purpose

The database stores persistent data for the cardiac.exe
e-commerce website.

The main data we need to store is:

- Users
- Products
- Shopping carts
- Cart items
- Orders
- Order items

---

# 2. Database

Database engine:

SQLite

Database access layer:

SQLAlchemy

Architecture:

Python / Flask
       ↓
SQLAlchemy
       ↓
SQLite

---

# 3. Tables

## 3.1 Users

Stores customer account information.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Unique user ID |
| email | TEXT | UNIQUE, NOT NULL | Customer email |
| password_hash | TEXT | NOT NULL | Hashed password |
| email_verified | BOOLEAN | NOT NULL | Whether email is verified |
| created_at | DATETIME | NOT NULL | Account creation time |

### Important decisions

Passwords are never stored as plaintext.

Only a secure password hash is stored.

Email addresses must be unique so that multiple accounts
cannot be created using the same email address.

---

# 4. Products

Stores products available for purchase.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Unique product ID |
| name | TEXT | NOT NULL | Product name |
| description | TEXT | | Product description |
| price | INTEGER | NOT NULL | Product price |
| stock | INTEGER | NOT NULL | Available quantity |
| image | TEXT | | Product image filename/path |
| category | TEXT | | Product category |
| created_at | DATETIME | NOT NULL | Product creation time |

### Important decisions

Prices will be stored as integer values representing
the smallest currency unit or, for our INR implementation,
whole rupee amounts.

Stock is stored so that the application can prevent
customers from ordering unavailable products.

---

# 5. Carts

Stores a customer's shopping cart.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Unique cart ID |
| user_id | INTEGER | FOREIGN KEY | User who owns the cart |
| created_at | DATETIME | NOT NULL | Cart creation time |

Relationship:

User 1 ──────── 1 Cart

---

# 6. CartItems

Stores individual products inside a cart.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Unique cart item ID |
| cart_id | INTEGER | FOREIGN KEY | Cart containing the item |
| product_id | INTEGER | FOREIGN KEY | Product being added |
| quantity | INTEGER | NOT NULL | Quantity requested |

Relationships:

Cart 1 ──────── many CartItems

Product 1 ────── many CartItems

---

# 7. Orders

Stores an order created by a customer.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Unique order ID |
| user_id | INTEGER | FOREIGN KEY | Customer who placed order |
| total_amount | INTEGER | NOT NULL | Total order value |
| status | TEXT | NOT NULL | Current order status |
| created_at | DATETIME | NOT NULL | Order creation time |

Possible statuses:

- pending
- confirmed
- processing
- shipped
- delivered
- cancelled

---

# 8. OrderItems

Stores the individual products that belong to an order.

| Column | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY | Unique order item ID |
| order_id | INTEGER | FOREIGN KEY | Associated order |
| product_id | INTEGER | FOREIGN KEY | Purchased product |
| quantity | INTEGER | NOT NULL | Quantity purchased |
| price | INTEGER | NOT NULL | Price at time of purchase |

### Why store price here?

The price of a product can change after an order is
created.

For example:

Product price today:

₹499

Customer places an order.

Later the product price changes:

₹599

The old order must still show:

₹499

Therefore OrderItems stores the price that existed
when the order was created.

---

# 9. Relationships

```text
Users
  │
  ├─────────────── Cart
  │                  │
  │                  └──── CartItems ───── Products
  │
  └─────────────── Orders
                     │
                     └──── OrderItems ──── Products

## 10 .
User
 │
 │ 1
 │
 └──────── 1 Cart

Cart
 │
 │ 1
 │
 └──────── many CartItems

Product
 │
 │ 1
 │
 └──────── many CartItems

User
 │
 │ 1
 │
 └──────── many Orders

Order
 │
 │ 1
 │
 └──────── many OrderItems

Product
 │
 │ 1
 │
 └──────── many OrderItems  

## 11. Security Considerations

The database must never store plaintext passwords.

Authentication-related data must be protected.

User authorization must be handled by the backend rather
than trusted from browser-provided data.

Product prices used for orders must be retrieved and
validated by the backend.

The client must not be trusted to determine:

Product price
User identity
Order ownership
Stock availability
Authorization status

## 12. Future Considerations

The following may be added later depending on project requirements:

Product variants
Multiple product images
Delivery addresses
Shipping information
Payment records
Discount codes
Admin users
Product reviews
Order tracking