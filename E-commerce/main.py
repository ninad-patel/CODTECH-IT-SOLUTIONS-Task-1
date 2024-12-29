import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, url_for, flash, session, redirect

mycursor =  None
connection = None
def conncheck():
    global mycursor
    global connection
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            database='nano',
            password='nanoninad'
        )
        mycursor = connection.cursor()
        return ("Successfully connected to the MySQL database")
    except Error as e:
        return ("Error while connecting to MySQL", e)

print(conncheck())

app = Flask(__name__)
app.secret_key = 'nano'

cart = []

@app.route('/')
def home():
    user_name = session.get('user_name') if session.get('logged_in') else None
    if 'user_name' not in session:
        return render_template('index.html')
    return render_template('index.html', user_name = user_name)

def authenticate_user(email, password):
    query = "SELECT * FROM data WHERE email = %s AND password = %s"
    values = (email, password)
    mycursor.execute(query, values)
    result = mycursor.fetchone()
    return result is not None

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_message = ""
    if request.method == 'POST':
        e = request.form['email']
        p = request.form['password']
        query = "SELECT name FROM data WHERE email=%s AND password=%s"
        values = (e, p)
        mycursor.execute(query, values)
        result = mycursor.fetchone()
        try:
            if authenticate_user(e, p):
                session['logged_in'] = True  # Set session variable
                session['user_name'] = result[0]  # Store user-specific data
                login_message = "Login successful! Welcome!"
                return redirect(url_for('home'))
            else:
                login_message = "Invalid email or password. Please try again."
        except Exception as error:
            login_message = f"An error occurred: {error}"
    return render_template('login.html', login_message=login_message)

def register_data(name, contact, email, password):
    query = "insert into data values(%s, %s, %s, %s)"
    values = (name, contact, email, password)
    mycursor.execute(query, values)
    result = mycursor.fetchall()
    connection.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        n = request.form['name']
        c = request.form['contact']
        e = request.form['email']
        p = request.form['password']
        try:
            register_data(n, c, e, p)
            flash("You have registered successfully!")
        except Exception as error:
            flash(f"An error occurred: {error}")
    return render_template('register.html')

@app.route('/reset')
def reset():
    return render_template('reset.html')

@app.route('/product/<int:product_id>')
def product_details(product_id):
    query = "SELECT * FROM products WHERE id = %s"
    mycursor.execute(query, (product_id,))
    product = mycursor.fetchone()
    user_name = session.get('user_name') if session.get('logged_in') else None
    if product:
        return render_template('product.html', product=product, user_name=user_name)
    else:
        flash("Product not found!")
        return redirect(url_for('home'))

@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    user_name = session.get('user_name') if session.get('logged_in') else None
    if 'user_name' not in session:
        return render_template('index.html')
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        cart.append(product_id)
        flash("Product added to cart!")
        return redirect(url_for('cart_page'))
    cart_products = []
    for product_id in cart:
        query = "SELECT * FROM products WHERE id = %s"
        mycursor.execute(query, (product_id,))
        product = mycursor.fetchone()
        if product:
            cart_products.append(product)
    return render_template('cart.html', cart_products=cart_products, user_name=user_name)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user_name = session.get('user_name') if session.get('logged_in') else None
    if 'user_name' not in session:
        return render_template('index.html')
    if request.method == 'POST':
        # Process checkout logic
        flash("Purchase completed successfully!")
        cart.clear()
        return redirect(url_for('home'))
    return render_template('checkout.html', cart_products=cart, user_name=user_name)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))

if(__name__ == '__main__'):
    app.run(debug=True)