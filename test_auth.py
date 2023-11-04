import firebase_admin
from firebase_admin import auth, credentials
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

cred = credentials.Certificate("tip-tours-df5b5-firebase-adminsdk-659l9-e5b2e8dd16.json")  # Replace with your service account key path
firebase_admin.initialize_app(cred)

def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(e)
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        decoded_token = verify_token(token)
        if not decoded_token:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({'message': 'You accessed the protected route!'})

if __name__ == '__main__':
    app.run(debug=True)
