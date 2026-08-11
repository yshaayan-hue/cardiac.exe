## System-Architecture 
        
                 CUSTOMER
                    │
                    ▼
             HTML / CSS / JS
                    │
                 HTTP
                    │
                    ▼
              ┌───────────┐
              │   Flask   │
              │  Backend  │
              └─────┬─────┘
                    │
                    |
                    │
                    ├── Authentication
                    ├── Products
                    ├── Cart
                    ├── Orders
                    └── Admin
                    ▼
               SQLAlchemy
                    │
                    ▼
                 SQLite
## - Core Logic 
Browser
   │
   │  Cookie
   ▼
Flask
   │
   ▼
   Session
   │
   ▼
Route
   │
   ▼
Application / Business Logic
   │
   ▼
SQLAlchemy
   │
   ▼
SQLite
   │
   ▼
SQLAlchemy
   │
   ▼
Application / Business Logic
   │
   ▼
Flask
   │
   ▼
HTML / JSON Response
   │
   ▼
Browser
 
## Component Responsibilities

### Browser

The browser displays the frontend and sends HTTP requests
to the Flask application.

It also stores cookies that can be used by the server to
identify a user's session.

The browser itself does not decide whether a user is
authorized. The server makes that decision.

### Flask

Flask is a Python web framework.

It receives HTTP requests, matches requests to routes,
executes our application code, and returns HTTP responses.

### Application / Business Logic

This is our Python code that contains the rules of the
application.

Examples:

- Checking whether a product exists
- Checking stock
- Calculating order totals
- Checking whether a user is allowed to perform an action

### SQLAlchemy

SQLAlchemy is a Python database toolkit/ORM.

It allows our Python application to communicate with the
database and work with database data using Python.

### SQLite

SQLite is the database engine that stores persistent
application data.

Examples include:

- Users
- Products
- Carts
- Cart items
- Orders

SQLite executes database queries and returns the requested
data.

### Sessions / Cookies

A session allows the server to remember information about
a user's interaction with the application.

A cookie stored by the browser can be used to identify
the user's session on subsequent requests.

### Email Service

The email service will be used to send account verification
emails to customers.

### WhatsApp

WhatsApp will be used as the initial communication channel
for submitting orders to the seller.

Payment and delivery will initially be handled privately
between the customer and seller.