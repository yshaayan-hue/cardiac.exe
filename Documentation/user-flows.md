# cardiac.exe — User Flows

## 1. Customer Browsing

Customer
    ↓
Open cardiac.exe
    ↓
View catalogue
    ↓
Browse products
    ↓
Select a product
    ↓
View product details

## 2. Customer
    ↓
Enter search query
    ↓
Frontend sends search request
    ↓
Flask receives request
    ↓
Search product data
    ↓
Return matching products
    ↓
Display results

## 3. Customer
    ↓
View product
    ↓
Click "Add to Cart"
    ↓
Flask validates product
    ↓
Check availability
    ↓
Add product to cart
    ↓
Return updated cart

## 4. Customer
    ↓
Click "Register"
    ↓
Enter email + password
    ↓
Submit registration
    ↓
Flask validates input
    ↓
Check whether email already exists
    ↓
Hash password
    ↓
Create account
    ↓
Generate email verification token
    ↓
Send verification email
    ↓
Customer verifies email
    ↓
Account becomes verified

## 5. Customer
    ↓
Receives verification email
    ↓
Clicks verification link
    ↓
Flask receives verification token
    ↓
Validate token
    ↓
Check token expiration
    ↓
Check whether token has already been used
    ↓
Verify account
    ↓
Token becomes invalid

## 6. Customer
    ↓
Enter email + password
    ↓
Submit login
    ↓
Flask finds account
    ↓
Verify password
    ↓
Check email verification
    ↓
Create authenticated session
    ↓
Customer logged in

## 7. Customer
    ↓
Click Logout
    ↓
Flask removes/invalidate session
    ↓
Customer becomes logged out

## 8. Customer
    ↓
Open Cart
    ↓
Retrieve cart
    ↓
Retrieve current product information
    ↓
Calculate server-side total
    ↓
Display cart

## 9. Customer
    ↓
Review cart
    ↓
Click "Order via WhatsApp"
    ↓
Flask validates cart
    ↓
Check products and availability
    ↓
Calculate server-side total
    ↓
Create order record
    ↓
Generate WhatsApp order message
    ↓
Open WhatsApp
    ↓
Seller receives order
    ↓
Seller confirms availability and final price
    ↓
Payment + delivery arranged privately

## 10. Administrator
    ↓
Open admin login
    ↓
Enter credentials
    ↓
Flask authenticates user
    ↓
Check admin authorization
    ↓
Create admin session
    ↓
Admin dashboard

## 11. Admin
    ↓
Admin dashboard
    ↓
Add product
    ↓
Enter product information
    ↓
Upload product image
    ↓
Flask validates data
    ↓
Save product
    ↓
Product appears in catalogue

# Edit product 
  Admin
    ↓
Select product
    ↓
Edit information
    ↓
Flask validates changes
    ↓
Update database
    ↓
Updated product appears on website

# Delete Product

   Admin
    ↓
Select product
    ↓
Request deletion
    ↓
Flask checks authorization
    ↓
Confirm deletion
    ↓
Remove/archive product

##12. Guest
Guest
 ↓
Browse products
 ↓
View product
 ↓
Add to cart

Logged-in customer

Customer
 ↓
Login
 ↓
Persistent account
 ↓
Cart associated with account
 ↓
Order history

##13 .
Request
   ↓
Validate input
   ↓
Check authentication
   ↓
Check authorization
   ↓
Perform operation
   ↓
Handle errors
   ↓
Return response


---

