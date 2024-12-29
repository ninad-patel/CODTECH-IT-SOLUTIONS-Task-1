# CODTECH-IT-SOLUTIONS-Task-1

Project Overview
It is an e-commerce website that enables user to browse products, add items to a shopping cart, and complete purchases. It is developed using html and css for front-end and python and flask framework for back-end. All the features and functionality of the website are as follows:

1. First of all, home page appear which consists of navbar with logo, search bar and cart and account icons, main page with the products' image and description and a footer with about us and contact us details.
2. A user can click on the product to know more about product. Product details is visible without login but a user can add that particular product to the cart only if he/she is logged in.
3. A user need to hover account icon to enable overlay of sign-in button which will redirect to the login page.
4. Once the user is logged in he/she can add the product to cart and click the checkout button which will redirect to the payment page. Now, he/she need to enter shipping address and select payment method.
5. When payment is done, click on complete puchase. It's done. Now, user can continue shopping or logout hovering account icon.

How all these functionality works?
1. When the program is run on localhost, home page appears i.e. index.html without user's name as user is not logged in. app route for home page checks the condition if the user is logged in or not. If logged in, user's name is visible with account icon.
2. When a user register on register.html page, /register route's method store that data into the mysql database using register data function.
3. When a user login on the login.html page, /login route's method checks the email and password using user_authentication function. If user email and password mathces with the data in the database, user is logged in and session is started.
4. When a user click on product's image, /product route's method fetch the data of the product from the database which is stored by the seller and then product detail is visible on product.html page.
5. When a user clicks on add to cart button, /cart route's method fetch the product in the database using product id and add the product id into cart list and all the product in the cart is visible on the cart.html page.
6. When a user clicks on checkout button, /checkout route's method opens checkout.html page. Once the purchase is completed, cart value become null using clear method.
7. When a user clicks logout after hovering to account icon, /logout route's method pop out all the session variable to clear the session. This will logout the user and redirect to the home page again without user's name.
