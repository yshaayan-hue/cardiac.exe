# Cart System — cardiac.exe

## 1. Purpose

The cart system allows a customer to:

- Add a product to the cart
- Increase product quantity
- Decrease product quantity
- Remove a product
- View subtotal
- View the total cart price
- Continue shopping when the cart is empty

The cart is currently stored using the Flask session.

---

# 2. How the Cart Works

The basic flow is:

Browser
    ↓
Flask Route
    ↓
Flask Session
    ↓
Database
    ↓
Cart Calculation
    ↓
Jinja Template
    ↓
Browser


Example:

Customer clicks "Add to Cart"

    ↓

GET /cart/add/1

    ↓

Flask receives product ID = 1

    ↓

SQLAlchemy finds Product 1

    ↓

Product ID is stored in the session

    ↓

Customer is redirected to /cart

    ↓

Flask calculates subtotal and total

    ↓

cart.html displays the result