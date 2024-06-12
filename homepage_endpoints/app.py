from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

app = Flask(__name__)

# Set up JWT
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

# Dummy user data (replace this with your actual user authentication logic)
users = {
    "username": "password"
}

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username not in users or users[username] != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Logout endpoint
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response, 200

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Sample unprotected routes
@app.route('/home', methods=['GET'])
def home():
    response = {"message": "Home page content"}
    return jsonify(response)

@app.route('/about',methods=['GET'])
def about():
    response = {"message": "About page content"}
    return jsonify(response)

@app.route('/contact',methods=['GET'])
def contact():
    response = {"message":'Contact page content'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
