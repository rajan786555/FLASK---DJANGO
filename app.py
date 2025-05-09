from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from flask_restful import Resource,Api
from flask import jsonify

app = Flask(__name__)
api=Api(app)
cart = {}
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to place an order.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Set the secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')  # Use an env variable for production

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Sample menu data
menu = {
    '1': {'name': 'Crispy Burger', 'price': 10.99},
    '2': {'name': 'Aloo Tikki Burger', 'price': 5.99},
    '3': {'name': 'Cheese Burger', 'price': 8.99},
    '4': {'name': 'Double Tikki Burger', 'price': 4.99},
    '5': {'name': 'Veggie burger', 'price': 7.99},
    '6': {'name': 'Simple burger', 'price': 6.99},
    '7': {'name': 'MAGGI BURGER', 'price': 2.99},
    '8': {'name': 'KULHAD PIZZA', 'price': 1.99},
    '9': {'name': 'VEG MOMOS', 'price': 3.99},
    '10': {'name': 'PANEER MOMOS', 'price': 3.99},
    '11': {'name': 'CHICKEN MOMOS', 'price': 3.99},
    '12': {'name': 'FISH MOMOS', 'price': 3.99},
    '13': {'name': 'KULHAD MOMOS', 'price': 3.99},
    '14': {'name': 'AFGHANI MOMOS', 'price': 3.99},
    '15': {'name': 'PANNER TIKKA', 'price': 3.99},
    '16': {'name': 'PANNER PIZZA', 'price': 3.99},
    '17': {'name': 'CHICKEN CHILLI', 'price': 3.99},
    '18': {'name': 'SANDWICH', 'price': 3.99},
    '20': {'name': 'GRILL SANDWICH', 'price': 3.99},
    '21': {'name': 'KULCHA', 'price': 3.99},
    '22': {'name': 'MOMOS', 'price': 3.99},
    '23': {'name': 'MOMOS', 'price': 3.99},
    '25': {'name': 'MOMOS', 'price': 3.99},
    '26': {'name': 'MOMOS', 'price': 3.99},
    '27': {'name': 'MOMOS', 'price': 3.99},
    '28': {'name': 'MOMOS', 'price': 3.99},
    '29': {'name': 'MOMOS', 'price': 3.99},
    '30': {'name': 'MOMOS', 'price': 3.99},
    '31': {'name': 'MOMOS', 'price': 3.99},
    '32': {'name': 'MOMOS', 'price': 3.99},
    '33': {'name': 'MOMOS', 'price': 3.99},
    '34': {'name': 'MOMOS', 'price': 3.99},
    '35': {'name': 'MOMOS', 'price': 3.99},
    '36': {'name': 'MOMOS', 'price': 3.99},
    '37': {'name': 'MOMOS', 'price': 3.99},
    '38': {'name': 'MOMOS', 'price': 3.99},
    '39': {'name': 'MOMOS', 'price': 3.99},
    '40': {'name': 'MOMOS', 'price': 3.99},
    '41': {'name': 'MOMOS', 'price': 3.99},
    '42': {'name': 'MOMOS', 'price': 3.99},
    '43': {'name': 'MOMOS', 'price': 3.99},
    '44': {'name': 'MOMOS', 'price': 3.99},
    '45': {'name': 'MOMOS', 'price': 3.99},
    '46': {'name': 'MOMOS', 'price': 3.99},
    '47': {'name': 'MOMOS', 'price': 3.99},
    '48': {'name': 'MOMOS', 'price': 3.99},
    '49': {'name': 'MOMOS', 'price': 3.99},
    '50': {'name': 'MOMOS', 'price': 3.99},
    '51': {'name': 'MOMOS', 'price': 3.99},
    '52': {'name': 'MOMOS', 'price': 3.99},
    '53': {'name': 'MOMOS', 'price': 3.99},
    '54': {'name': 'MOMOS', 'price': 3.99},
    '55': {'name': 'MOMOS', 'price': 3.99},
    '56': {'name': 'MOMOS', 'price': 3.99},
    '57': {'name': 'MOMOS', 'price': 3.99},
    '58': {'name': 'MOMOS', 'price': 3.99},
    '59': {'name': 'MOMOS', 'price': 3.99},
    '60': {'name': 'MOMOS', 'price': 3.99},
    '61': {'name': 'MOMOS', 'price': 3.99},
    '62': {'name': 'MOMOS', 'price': 3.99},
    '63': {'name': 'MOMOS', 'price': 3.99},
    '64': {'name': 'MOMOS', 'price': 3.99},
    '65': {'name': 'MOMOS', 'price': 3.99},
    '66': {'name': 'MOMOS', 'price': 3.99},
}
@app.route('/logout')
def logout():
    # Your logout logic here
    return redirect(url_for('index'))  # or wherever you want to redirect after logout

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     data = request.get_json()
#     item_id = str(data.get('id'))
#     item_name = data.get('name')

#     if item_id in cart:
#         cart[item_id]['quantity'] += 1  # Increase quantity if already in cart
#     else:
#         cart[item_id] = {'name': item_name, 'quantity': 1}

#     return jsonify(cart)  # Return updated cart

@app.route('/get_cart', methods=['GET'])
def get_cart():
    return jsonify(cart)  # Send cart data to frontend

@app.route('/menu')
def show_menu():
    return render_template('menu.html', menu=menu)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    
    if item_id in cart:
        cart[item_id]['quantity'] += 1
    else:
        cart[item_id] = {'name': menu[item_id]['name'], 'price': menu[item_id]['price'], 'quantity': 1}
    
    session['cart'] = cart  # Ensure session updates
    session.modified = True  # Mark session as modified
    return redirect(url_for('show_cart'))
    
# @app.route('/remove_from_cart', methods=['POST'])
# def remove_from_cart():
#     data = request.get_json()
#     item_id = str(data.get('id'))

#     if item_id in cart:
#         cart[item_id]['quantity'] -= 1  # Decrease quantity
#         if cart[item_id]['quantity'] <= 0:
#             del cart[item_id]  # Remove if quantity is 0

#     return jsonify(cart)  # Return updated cart    
    
@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    data = request.get_json()
    item_id = str(data.get('id'))

    if item_id in cart:
        del cart[item_id]  # Remove item from cart

    return jsonify(cart)  # Return updated cart    

@app.route('/cart')
def show_cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = request.form.get('item_id')
    if 'cart' in session and item_id in session['cart']:
        del session['cart'][item_id]
    session.modified = True
    return redirect(url_for('show_cart'))
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty. Please add items to your cart before placing an order.')
        return redirect(url_for('show_menu'))
    
    # Process the order here (save to database, etc.)
    session.pop('cart', None)  # Clear the cart after placing the order
    flash('Order placed successfully!')
    return render_template('order_confirmation.html')

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already in use.', 'danger')
            return redirect(url_for('signup'))

        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('show_menu'))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/wheel')
def scaners():
    return render_template('wheel.html')

@app.route('/success')
def success():
    flash("Successfully logged in!")
    return redirect(url_for('index'))  # You should redirect to the home page after a successful action


class SignupAPI(Resource):
    def post(self):
        if not request.is_json:
            return {'message': 'Request must be in JSON format'}, 400

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return {'message': 'All fields are required'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 409

        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


class LoginAPI(Resource):
    def post(self):
        if not request.is_json:
            return {'message': 'Request must be in JSON format'}, 400

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return {'message': 'Email and password are required'}, 400

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return {'message': 'Login successful'}
        return {'message': 'Invalid credentials'}, 401
    
class ContactAPI(Resource):
    def get(self):
        messages = Contact.query.all()
        return [{'id': msg.id, 'name': msg.name, 'email': msg.email, 'message': msg.message} for msg in messages]

    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            return {'message': 'All fields are required!'}, 400

        new_message = Contact(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return {'message': 'Your message has been sent successfully!'}, 201
    
class MenuAPI(Resource):
    def get(self):
        return menu

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data:
            return {'message': 'Name and price are required'}, 400

        new_id = str(max([int(key) for key in menu.keys() if key.isdigit()] + [0]) + 1)
        menu[new_id] = {'name': data['name'], 'price': float(data['price'])}
        return {'id': new_id, 'item': menu[new_id]}, 201


class MenuItemAPI(Resource):
    def get(self, item_id):
        if item_id not in menu:
            return {'message': 'Item not found'}, 404
        return menu[item_id]

    def put(self, item_id):
        if item_id not in menu:
            return {'message': 'Item not found'}, 404

        data = request.get_json()
        if not data:
            return {'message': 'No data provided'}, 400

        if 'name' in data:
            menu[item_id]['name'] = data['name']
        if 'price' in data:
            menu[item_id]['price'] = float(data['price'])
        return menu[item_id]

    def delete(self, item_id):
        if item_id not in menu:
            return {'message': 'Item not found'}, 404
        deleted = menu.pop(item_id)
        return {'message': 'Item deleted successfully', 'item': deleted}


class CartAPI(Resource):
    def get(self):
        if 'username' not in session:
            return {'message': 'Login required'}, 403
        return session.get('cart', {})

    def post(self):
        if 'username' not in session:
            return {'message': 'Login required'}, 403

        data = request.get_json()
        item_id = str(data.get('item_id'))

        if item_id not in menu:
            return {'message': 'Item not found'}, 404

        if 'cart' not in session:
            session['cart'] = {}
        cart = session['cart']

        if item_id in cart:
            cart[item_id]['quantity'] += 1
        else:
            cart[item_id] = {
                'name': menu[item_id]['name'],
                'price': menu[item_id]['price'],
                'quantity': 1
            }
        session.modified = True
        return {'message': 'Item added to cart'}

    def delete(self):
        if 'username' not in session:
            return {'message': 'Login required'}, 403

        data = request.get_json()
        item_id = str(data.get('item_id'))
        cart = session.get('cart', {})

        if item_id in cart:
            del cart[item_id]
            session.modified = True
            return {'message': 'Item removed from cart'}
        return {'message': 'Item not in cart'}, 404


class PlaceOrderAPI(Resource):
    def post(self):
        if 'cart' not in session or not session['cart']:
            return {'message': 'Cart is empty'}, 400
        session.pop('cart', None)
        return {'message': 'Order placed successfully'}



api.add_resource(SignupAPI, '/api/signup')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(ContactAPI, '/api/contact')
api.add_resource(MenuAPI, '/api/menu')
api.add_resource(MenuItemAPI, '/api/menu/<string:item_id>')
api.add_resource(CartAPI, '/api/cart')
api.add_resource(PlaceOrderAPI, '/api/place_order')



if __name__ == '__main__':
    app.run(debug=True)
