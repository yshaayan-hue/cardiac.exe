# cardiac.exe — Requirements

## 1. Project Overview

cardiac.exe is an online storefront for custom-designed
collectible cards.

The business creates original/custom card designs that can
be displayed and ordered through the website.

The website will allow customers to browse card designs,
view product information, add cards to a cart, create an
account, and submit orders through WhatsApp.

Payment and delivery will initially be arranged privately
between the customer and the seller.

The final commercial card designs should avoid unauthorized
use of third-party trademarks, copyrighted artwork, logos,
characters, and other protected material.

## 2. Project Goals

### Primary goals

- Provide an online catalogue of trading cards.
- Allow customers to view individual products.
- Allow customers to add products to a cart.
- Allow customers to create an account.
- Verify customer email addresses.
- Allow customers to log in and log out.
- Allow customers to submit orders through WhatsApp.
- Provide the seller with a way to manage products.

### Learning goals

This project will also be used to learn:

- Flask
- HTTP
- HTML/CSS/JavaScript
- JSON
- SQL
- SQLAlchemy
- Databases
- Authentication
- Sessions
- Cookies
- Email verification
- API design
- Security
- Testing
- Debugging
- Deployment

---

## 3. Technology Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### Database

- SQLite
- SQLAlchemy

### Ordering

- WhatsApp

### Payment

- No online payment gateway in V1.

---

## 4. Customer Features

- Browse products
- Search products
- View product details
- Add products to cart
- Change cart quantity
- Remove products from cart
- Register
- Verify email
- Login
- Logout
- Maintain a cart
- Submit an order through WhatsApp

---

## 5. Admin Features

The administrator should eventually be able to:

- Login
- Add products
- Edit products
- Remove products
- Change product prices
- Update stock
- Upload product images
- View customer orders/enquiries

---

## 6. Payment

Online payment will NOT be implemented in V1.

The website will communicate that payment and delivery
are arranged privately with the seller.

This reduces the security and implementation complexity
of the first version.

---

## 7. Ordering

The initial ordering process will be:

Customer
    ↓
Browse products
    ↓
Add products to cart
    ↓
Review cart
    ↓
Generate WhatsApp order
    ↓
Seller confirms availability and price
    ↓
Payment + delivery arranged privately

---

## 8. Authentication

Customers will be able to:

- Create an account
- Verify their email
- Login
- Logout

Passwords must never be stored as plain text.

The system will use secure password hashing.

---

## 9. Security Requirements

The application must consider:

- Password security
- Session security
- Cookie security
- Input validation
- SQL injection
- Cross-site scripting (XSS)
- CSRF
- Authentication
- Authorization
- Secure secret management
- Rate limiting where appropriate

---

## 10. Out of Scope for V1

The following are not currently planned:

- Online payment gateway
- Automated delivery tracking
- Complex recommendation system
- Marketplace functionality
- Multiple sellers