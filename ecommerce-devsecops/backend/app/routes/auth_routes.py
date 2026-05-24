from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middleware.security import require_auth, validate_json_request
from app.security.auth import AuthenticationUtil, ValidationUtil
from app.middleware.logging import log_security_event, log_audit_event
import logging

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = logging.getLogger(__name__)

# Mock user database (replace with MongoDB in production)
users_db = {}

@bp.route('/register', methods=['POST'])
@validate_json_request
def register(data):
    """
    User registration endpoint
    
    POST /api/auth/register
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    try:
        email = data.get('email', '').strip()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        # Validation
        if not email or not password or not first_name or not last_name:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Missing required fields: email, password, first_name, last_name'
            }), 422
        
        if not ValidationUtil.validate_email(email):
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Invalid email format'
            }), 422
        
        if email in users_db:
            log_security_event('DUPLICATE_USER_REGISTRATION', email, 'Attempted duplicate registration', 'WARNING')
            return jsonify({
                'error': 'CONFLICT',
                'message': 'User already exists'
            }), 409
        
        is_valid, msg = ValidationUtil.validate_password(password)
        if not is_valid:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': msg
            }), 422
        
        # Create user
        hashed_password = AuthenticationUtil.hash_password(password)
        users_db[email] = {
            'email': email,
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name,
            'roles': ['user'],
            'created_at': str(__import__('datetime').datetime.utcnow())
        }
        
        log_audit_event('USER_REGISTERED', email, 'user', {'email': email})
        log_security_event('USER_REGISTRATION_SUCCESS', email, 'New user registered', 'INFO')
        
        return jsonify({
            'message': 'User registered successfully',
            'email': email
        }), 201
    
    except Exception as e:
        logger.error(f'Registration error: {str(e)}')
        log_security_event('REGISTRATION_ERROR', request.remote_addr, str(e), 'ERROR')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Registration failed'
        }), 500

@bp.route('/login', methods=['POST'])
@validate_json_request
def login(data):
    """
    User login endpoint
    
    POST /api/auth/login
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not email or not password:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Email and password required'
            }), 422
        
        if email not in users_db:
            log_security_event('LOGIN_FAILED_USER_NOT_FOUND', email, f'IP: {request.remote_addr}', 'WARNING')
            return jsonify({
                'error': 'AUTHENTICATION_ERROR',
                'message': 'Invalid email or password'
            }), 401
        
        user = users_db[email]
        if not AuthenticationUtil.verify_password(password, user['password']):
            log_security_event('LOGIN_FAILED_INVALID_PASSWORD', email, f'IP: {request.remote_addr}', 'WARNING')
            return jsonify({
                'error': 'AUTHENTICATION_ERROR',
                'message': 'Invalid email or password'
            }), 401
        
        # Create tokens
        access_token, refresh_token = AuthenticationUtil.create_tokens(
            email, 
            email, 
            roles=user['roles']
        )
        
        log_audit_event('USER_LOGIN', email, 'user', {})
        log_security_event('LOGIN_SUCCESS', email, f'IP: {request.remote_addr}', 'INFO')
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'email': email,
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'roles': user['roles']
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        log_security_event('LOGIN_ERROR', request.remote_addr, str(e), 'ERROR')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Login failed'
        }), 500

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    
    POST /api/auth/refresh
    Headers: Authorization: Bearer <refresh_token>
    """
    try:
        current_user = get_jwt_identity()
        
        if current_user not in users_db:
            return jsonify({
                'error': 'AUTHENTICATION_ERROR',
                'message': 'User not found'
            }), 401
        
        user = users_db[current_user]
        access_token, _ = AuthenticationUtil.create_tokens(
            current_user,
            current_user,
            roles=user['roles']
        )
        
        log_audit_event('TOKEN_REFRESH', current_user, 'auth_token', {})
        
        return jsonify({
            'access_token': access_token
        }), 200
    
    except Exception as e:
        logger.error(f'Token refresh error: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Token refresh failed'
        }), 500

@bp.route('/verify', methods=['GET'])
@require_auth
def verify_token(current_user):
    """
    Verify access token
    
    GET /api/auth/verify
    Headers: Authorization: Bearer <access_token>
    """
    try:
        if current_user not in users_db:
            return jsonify({
                'error': 'AUTHENTICATION_ERROR',
                'message': 'User not found'
            }), 401
        
        user = users_db[current_user]
        return jsonify({
            'valid': True,
            'user': {
                'email': current_user,
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'roles': user['roles']
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Token verification error: {str(e)}')
        return jsonify({
            'error': 'AUTHENTICATION_ERROR',
            'message': 'Invalid token'
        }), 401
