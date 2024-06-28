from flask import Flask, request, jsonify
import re
import sqlite3

app = Flask(__name__)

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if they do not exist
with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT,
                     email TEXT UNIQUE,
                     password TEXT,
                     phone TEXT
                     )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS merchants (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     business_name TEXT UNIQUE,
                     contact_person_name TEXT,
                     username TEXT UNIQUE,
                     email TEXT UNIQUE,
                     password TEXT,
                     phone TEXT,
                     bank_name TEXT,
                     account_number TEXT,
                     preferred_payment_methods TEXT,
                     business_license BLOB,
                     id_image BLOB,
                     agree_terms BOOLEAN
                     )''')

# Function to validate email format
def validate_email(email):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

# Function to validate password format
def validate_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)

# Function to validate phone number format
def validate_phone(phone):
    phone_regex = r'^07\d{8}$'
    return re.match(phone_regex, phone)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400

    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    email = data.get('email')
    phone = data.get('phone')

    # Validate inputs
    if not username or len(username) < 4:
        return jsonify({'error': 'Username must be at least 4 characters long'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if not validate_phone(phone):
        return jsonify({'error': 'Phone number must be in the format 07XXXXXXXX'}), 400

    # Insert user into database
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)",
                         (username, email, password, phone))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User with this email already exists'}), 400

    return jsonify({'message': 'Registration successful! Please login.'}), 201

@app.route('/merchant_signup', methods=['POST'])
def merchant_signup():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400

    business_name = data.get('businessName')
    contact_person_name = data.get('contactPersonName')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    email = data.get('email')
    phone = data.get('phone')
    bank_name = data.get('bankName')
    account_number = data.get('accountNumber')
    preferred_payment_methods = data.get('preferredPaymentMethods')
    business_license = data.get('businessLicense')
    id_image= data.get('id_image')
    agree_terms = data.get('agreeTerms')

    # Validate inputs
    if not business_name or len(business_name) < 4:
        return jsonify({'error': 'Business name is required and must be at least 4 characters long'}), 400

    if not contact_person_name:
        return jsonify({'error': 'Contact person name is required'}), 400

    if not username or len(username) < 4:
        return jsonify({'error': 'Username must be at least 4 characters long'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if not validate_phone(phone):
        return jsonify({'error': 'Phone number must be in the format 07XXXXXXXX'}), 400

    if not bank_name:
        return jsonify({'error': 'Bank name is required'}), 400

    if not account_number:
        return jsonify({'error': 'Account number is required'}), 400

    if not preferred_payment_methods:
        return jsonify({'error': 'Preferred payment method is required'}), 400

    if not business_license:
        return jsonify({'error': 'Business license is required'}), 400

    if not id_image:
        return jsonify({'error': 'ID proof is required'}), 400

    if agree_terms not in ['yes', 'no']:
        return jsonify({'error': 'You must agree to the terms and conditions with yes or no'}), 400

    agree_terms_bool = True if agree_terms == 'yes' else False

    # Insert merchant into database
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO merchants (business_name, contact_person_name, username, email, password, phone, bank_name, account_number, preferred_payment_methods, business_license, id_image, agree_terms) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (business_name, contact_person_name, username, email, password, phone, bank_name, account_number, preferred_payment_methods, business_license, id_image, agree_terms))
            conn.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Merchant with this email or username already exists'}), 400

    return jsonify({'message': 'Merchant registration successful! Please login.'}), 201

if __name__ == '__main__':
    app.run(debug=True)
