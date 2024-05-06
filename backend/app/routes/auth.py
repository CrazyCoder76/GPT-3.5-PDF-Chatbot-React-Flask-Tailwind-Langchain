from flask import Blueprint, request, send_from_directory
from ..models.User import User
from .. import bcrypt
from .. import db
from app import Config
from auth_middleware import token_required

import re
import jwt
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def validate_email_and_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None or user.password is None:
        return None
    if bcrypt.check_password_hash(user.password, password) is False:
        return None
    return user

@auth_bp.route('/user_info', methods=['POST'])
@token_required
def user_info(current_user):
    return {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email
    }

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']
    if not email or not password or not first_name or not last_name:
        return {'message': 'Fill all fields'}, 400
    if len(password) < 6:
        return {'message' : 'Password length must be at least 6!'}, 400
    user = User.query.filter_by(email=email).first()
    if user != None:
        return {'message' : 'Same email already exists'}, 400
    if not is_valid_email(email):
        return {'message' : 'Not valid email'}, 400
    # Here you would normally hash the password before saving
    user = User(
        email = email,
        password = bcrypt.generate_password_hash(password, 10).decode('utf-8'),
        first_name = first_name,
        last_name = last_name
    )
    db.session.add(user)
    db.session.commit()
    return {}

@auth_bp.route('/login', methods = ['POST'])
def login():
    data = request.json
    if not data:
        return {"message": "Please provide user details!",}, 400
    validated_user = validate_email_and_password(data['email'], data['password'])
    if validated_user is None:
        return {'message' : 'Credentials not correct!'}, 401
    
    token = jwt.encode({
        'user_id' : validated_user.id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY)
    
    return {'token' : token, 'user': {
        'id': validated_user.id,
        'email': validated_user.email,
        'first_name': validated_user.first_name,
        'last_name': validated_user.last_name
    }}

@auth_bp.route('/oauth', methods = ['POST'])
def oauth():
    token = request.json['credential']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), Config.GOOGLE_CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        user_id = idinfo['sub']
        
        # You can also get other information from the token
        email = idinfo.get('email')
        user = User.query.filter_by(email=email).first()
        first_name, last_name = '', ''
        if user is None:
            name = idinfo.get('name')
            first_name,last_name = name.split(' ')
            user = User(
                email = email,
                first_name = first_name,
                last_name = last_name
            )
            db.session.add(user)
            db.session.commit()
        else:
            first_name, last_name = user.first_name, user.last_name
            # You might want to create a user in your DB with this information, or update an existing one
        token = jwt.encode({
            'user_id' : user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
            }, Config.SECRET_KEY)
        return {
            'token' : token,
            'user': {
                'id': user.id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name}
            }, 200
    except ValueError:
        # Invalid token
        pass
    return {'message':"Token is invalid or expired"}, 401

@auth_bp.route('/avatar/<img_id>')
def get_image(img_id):
    return send_from_directory('avatar', img_id)