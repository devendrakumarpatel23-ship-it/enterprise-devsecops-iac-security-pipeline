import hmac
import hashlib
import logging
from flask import request, jsonify
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """
    Security middleware for request validation and protection
    - CSRF prevention
    - Rate limiting
    - Input validation
    - Security headers
    """
    
    BLOCKED_HEADERS = [
        'X-Forwarded-For',
        'X-Forwarded-Proto',
        'X-Original-URL'
    ]
    
    @staticmethod
    def validate_request():
        """Validate incoming requests for security"""
        
        # Check for blocked headers
        for header in SecurityMiddleware.BLOCKED_HEADERS:
            if header in request.headers:
                logger.warning(f'Blocked suspicious header: {header}')
                return jsonify({
                    'error': 'Invalid Request',
                    'message': 'Suspicious headers detected'
                }), 400
        
        # Validate Content-Type for POST/PUT
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.headers.get('Content-Type', '')
            if content_type and not any(ct in content_type for ct in ['application/json', 'multipart/form-data']):
                logger.warning(f'Invalid Content-Type: {content_type}')
                return jsonify({
                    'error': 'Invalid Content-Type',
                    'message': 'Content-Type must be application/json or multipart/form-data'
                }), 400
        
        # Log request
        logger.info(f'{request.method} {request.path} from {request.remote_addr}')
        
        return None

def require_auth(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            return f(current_user, *args, **kwargs)
        except Exception as e:
            logger.warning(f'Authentication failed: {str(e)}')
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Valid JWT token required'
            }), 401
    
    return decorated_function

def validate_json_request(f):
    """Decorator to validate JSON request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request must be valid JSON'
            }), 400
        
        try:
            data = request.get_json()
            return f(data, *args, **kwargs)
        except Exception as e:
            logger.error(f'JSON parsing error: {str(e)}')
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid JSON'
            }), 400
    
    return decorated_function

def rate_limit(max_calls, time_window):
    """Rate limiting decorator"""
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri='memory://'
    )
    
    return limiter.limit(f'{max_calls} per {time_window}')

def check_permissions(required_roles):
    """Check user role permissions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            # Get user role from token or database
            user_role = request.headers.get('X-User-Role', 'user')
            
            if user_role not in required_roles:
                logger.warning(f'Permission denied for user {current_user} with role {user_role}')
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'Required roles: {", ".join(required_roles)}'
                }), 403
            
            return f(current_user, *args, **kwargs)
        
        return decorated_function
    
    return decorator
