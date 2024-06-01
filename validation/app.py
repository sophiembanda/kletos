from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy data for existing users
users = {
    'john.doe@example.com': 'Password123!',
    'jane.smith@example.com': 'SecureP@ss1'
}

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        print("POST request received for signup")
        print("Form data:", request.form)

        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Validate username
        if not username or len(username) < 4:
            flash('Username must be at least 4 characters long.', 'error')
            return render_template('signup.html', username=username, email=email, phone=phone)

        if email in users:
            flash('Email already exists.', 'error')
            return render_template('signup.html', username=username, email=email, phone=phone)

        # Validate email
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not email or not re.match(email_regex, email):
            flash('Invalid email format.', 'error')
            return render_template('signup.html', username=username, email=email, phone=phone)

        # Validate password
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not password or not re.match(password_regex, password):
            flash('Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character.', 'error')
            return render_template('signup.html', username=username, email=email, phone=phone)

        if not confirm_password or password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html', username=username, email=email, phone=phone)

        # Validate phone number and convert to international format
        phone_regex = r'^07\d{8}$'
        if not phone or not re.match(phone_regex, phone):
            flash('Phone number must be in the format 07XXXXXXXX.', 'error')
            return render_template('signup.html', username=username, email=email, phone=phone)

        international_phone = '+254' + phone[1:]  # Convert to +254XXXXXXXXX

        # If all validations pass
        users[email] = password
        flash(f'Registration successful! Your phone number is {international_phone}', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/merchant_signup', methods=['POST'])
def merchant_signup():
    if request.method == 'POST':
        print("POST request received for merchant signup")
        print("Form data:", request.form)

        business_name = request.form.get('businessName')
        contact_person_name = request.form.get('contactPersonName')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        email = request.form.get('email')
        phone = request.form.get('phone')
        bank_name = request.form.get('bankName')
        account_number = request.form.get('accountNumber')
        preferred_payment_methods = request.form.get('preferredPaymentMethods')
        business_license = request.files.get('businessLicense')
        id_proof = request.files.get('idProof')
        agree_terms = request.form.get('agreeTerms')

        # Validate business name
        if not business_name:
            flash('Business name is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate contact person name
        if not contact_person_name:
            flash('Contact person name is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate username
        if not username or len(username) < 4:
            flash('Username must be at least 4 characters long.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        if email in users:
            flash('Email already exists.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate email
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not email or not re.match(email_regex, email):
            flash('Invalid email format.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate password
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not password or not re.match(password_regex, password):
            flash('Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        if not confirm_password or password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate phone number and convert to international format
        phone_regex = r'^07\d{8}$'
        if not phone or not re.match(phone_regex, phone):
            flash('Phone number must be in the format 07XXXXXXXX.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        international_phone = '+254' + phone[1:]  # Convert to +254XXXXXXXXX

        # Validate bank details
        if not bank_name:
            flash('Bank name is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        if not account_number:
            flash('Account number is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate preferred payment methods
        if not preferred_payment_methods:
            flash('Preferred payment method is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate business license upload
        if not business_license:
            flash('Business license is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate ID proof upload
        if not id_proof:
            flash('ID proof is required.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # Validate agree to terms
        if not agree_terms:
            flash('You must agree to the terms and conditions.', 'error')
            return render_template('merchant_signup.html', business_name=business_name, contact_person_name=contact_person_name,
                                   username=username, email=email, phone=phone, bank_name=bank_name, account_number=account_number,
                                   preferred_payment_methods=preferred_payment_methods)

        # If all validations pass
        users[email] = password
        flash(f'Registration successful! Your phone number is {international_phone}', 'success')
        return redirect(url_for('login'))

    return render_template('merchant_signup.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print("POST request received for login")
        print("Form data:", request.form)

        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')

        # Validate email
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za.z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, email):
            flash('Invalid email format.', 'error')
            return render_template('login.html')

        # Validate user credentials
        if email not in users or users[email] != password:
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        # If credentials are correct
        flash('Login successful!', 'success')
        return redirect(url_for('signup'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
