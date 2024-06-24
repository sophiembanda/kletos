from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configure your app with a secret key and SQLAlchemy database URI
app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the JWT manager and SQLAlchemy
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Define the Cart and CartItem models
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

# Create the database and tables
with app.app_context():
    db.create_all()

# Sample data (optional)
with app.app_context():
    if not Product.query.first():
        sample_products = [
            Product(name="Product 1", category="Necklace", image="image_url_1", price=100.0),
            Product(name="Product 2", category="Bracelet", image="image_url_2", price=50.0),
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()

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
    current_user = get_jwt_identity()
    user_profile = {
        "id": 1,
        "name": "John Doe",
        "email": current_user
    }
    return jsonify({"user": user_profile})

@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Mock sign-in logic
    if email == "john.doe@example.com" and password == "password123":
        access_token = create_access_token(identity=email)
        return jsonify({"message": "User signed in", "token": access_token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/sign-out', methods=['POST'])
def sign_out():
    return jsonify({"message": "User signed out"})

# Hero Section Endpoint
@app.route('/hero-content', methods=['GET'])
def hero_content():
    hero = {
        "image": "banner_image_url",
        "text": "Kletos: Jewelry for Every Chapter",
        "button_text": "Learn More",
        "button_link": "/learn-more"
    }
    return jsonify({"hero": hero})

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
@app.route('/featured-products', methods=['GET'])
def get_featured_products():
    # Mock featured products
    featured_products = [
        {
            "id": 1,
            "name": "Featured Product 1",
            "image": "image_url",
            "price": 120.0
        },
    ]
    return jsonify({"featured_products": featured_products})

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

# Footer Endpoint
@app.route('/footer-content', methods=['GET'])
def footer_content():
    footer_content = {
        "about": "Find pieces that shimmer and radiate confidence just like you.",
        "links": [
            {"name": "Home", "url": "/home"},
            {"name": "Products", "url": "/products"},
        ],
        "contact": {
            "email": "support@kletos.com",
            "phone": "+1234567890",
            "address": "1234 Kletos St Jewelry City 56789"
        }
    }
    return jsonify({"footer": footer_content})

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
