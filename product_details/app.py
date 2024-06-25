from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Configure your app with a secret key and SQLAlchemy database URI
app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the JWT manager and SQLAlchemy
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Cart and CartItem models
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, default=0.0)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship('Cart', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('items', lazy=True))

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create the database and tables
with app.app_context():
    db.create_all()

# Sample data
with app.app_context():
    if not Product.query.first():
        sample_products = [
            Product(name="Product 1", category="Necklace", image="image_url_1", price=100.0),
            Product(name="Product 2", category="Bracelet", image="image_url_2", price=50.0),
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()

# Function to validate input
def validate_input(email_or_phone, password):
    if not email_or_phone or not password:
        return False, "Email or phone and password are required."
    return True, "Valid input"

# Function to generate token
def generate_token(user_id):
    return create_access_token(identity=user_id)

# Register Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    # Validate input
    if not email or not phone_number or not password:
        return jsonify({'error': 'Email, phone number, and password are required'}), 400

    # Check if user already exists
    if User.query.filter((User.email == email) | (User.phone_number == phone_number)).first():
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create new user
    new_user = User(email=email, phone_number=phone_number, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')

    # Validate input
    if not email_or_phone or not password:
        return jsonify({'error': 'Email or phone and password are required'}), 400

    # Find user by email or phone number
    user = User.query.filter((User.email == email_or_phone) | (User.phone_number == email_or_phone)).first()

    # Check if user exists and password is correct
    if user and user.check_password(password):
        token = generate_token(user.id)
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# Navigation Bar Endpoints
@app.route('/home', methods=['GET'])
def home():
    return jsonify({"message": "Home page content"})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = [
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "image": product.image,
            "price": product.price
        } for product in products
    ]
    return jsonify({"products": products_list})

@app.route('/about', methods=['GET'])
def about():
    return jsonify({"message": "About page content"})

@app.route('/contact', methods=['GET'])
def contact():
    return jsonify({"message": "Contact page content"})

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    user_profile = {
        "id": user.id,
        "email": user.email,
        "phone_number": user.phone_number
    }
    return jsonify({"user": user_profile})

@app.route('/sign-out', methods=['POST'])
def sign_out():
    # Perform sign-out logic here
    return jsonify({"message": "User signed out"})

# Category Navigation Endpoints
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = ["Necklace", "Bracelet", "Rings", "Earrings"]
    return jsonify({"categories": categories})

@app.route('/products-by-category', methods=['GET'])
def get_products_by_category():
    category_name = request.args.get('category')
    products = Product.query.filter_by(category=category_name).all()
    filtered_products = [
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "image": product.image,
            "price": product.price
        } for product in products
    ]
    return jsonify({"products": filtered_products, "category": category_name})

# Featured Products Endpoint
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_data = {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "image": product.image,
        "price": product.price
    }
    return jsonify({"product": product_data})

# Main Product Highlight Endpoint
@app.route('/highlighted-product', methods=['GET'])
def get_highlighted_product():
    highlighted_product = {
        "id": 2,
        "name": "Highlighted Product",
        "description": "This is the main highlighted product.",
        "image": "highlighted_image_url",
        "price": 150.0
    }
    return jsonify({"highlighted_product": highlighted_product})

# Cart Management Endpoints
@app.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    cart = Cart.query.first()
    if not cart:
        cart = Cart()
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    product = Product.query.get_or_404(product_id)
    cart.total_price += product.price * quantity

    db.session.commit()

    return jsonify({
        "message": "Product added to cart",
        "cart": {
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity
                } for item in CartItem.query.filter_by(cart_id=cart.id).all()
            ]
        }
    })

@app.route('/cart', methods=['GET'])
@jwt_required()
def fetch_cart():
    cart = Cart.query.first()
    if not cart:
        return jsonify({"cart": {"items": [], "total_price": 0}})

    items = []
    for item in CartItem.query.filter_by(cart_id=cart.id).all():
        product = Product.query.get(item.product_id)
        items.append({
            "product_id": item.product_id,
            "name": product.name,
            "quantity": item.quantity,
            "price": product.price,
            "total": product.price * item.quantity
        })

    return jsonify({
        "cart": {
            "items": items,
            "total_price": cart.total_price
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
