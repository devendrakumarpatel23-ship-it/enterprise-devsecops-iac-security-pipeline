from flask import Blueprint, request, jsonify
from app.middleware.security import require_auth, validate_json_request
from app.middleware.logging import log_audit_event
from app.security.auth import ValidationUtil, AuthenticationUtil
import logging

bp = Blueprint('users', __name__, url_prefix='/api/users')
logger = logging.getLogger(__name__)

# Mock user database (shared with auth_routes)
users_db = {}

@bp.route('/profile', methods=['GET'])
@require_auth
def get_profile(current_user):
    """
    Get user profile
    
    GET /api/users/profile
    Headers: Authorization: Bearer <token>
    """
    try:
        if current_user not in users_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'User not found'
            }), 404
        
        user = users_db[current_user]
        
        # Remove password from response
        user_data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'roles': user['roles'],
            'created_at': user.get('created_at')
        }
        
        return jsonify({
            'data': user_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching profile: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to fetch profile'
        }), 500

@bp.route('/profile', methods=['PUT'])
@require_auth
@validate_json_request
def update_profile(current_user, data):
    """
    Update user profile
    
    PUT /api/users/profile
    {
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    try:
        if current_user not in users_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'User not found'
            }), 404
        
        user = users_db[current_user]
        
        # Update allowed fields
        if 'first_name' in data:
            first_name = data['first_name'].strip()
            if not first_name:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'First name cannot be empty'
                }), 422
            user['first_name'] = first_name
        
        if 'last_name' in data:
            last_name = data['last_name'].strip()
            if not last_name:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Last name cannot be empty'
                }), 422
            user['last_name'] = last_name
        
        log_audit_event('PROFILE_UPDATED', current_user, 'user_profile', data)
        
        user_data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'roles': user['roles']
        }
        
        return jsonify({
            'message': 'Profile updated successfully',
            'data': user_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error updating profile: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to update profile'
        }), 500

@bp.route('/password', methods=['PUT'])
@require_auth
@validate_json_request
def change_password(current_user, data):
    """
    Change user password
    
    PUT /api/users/password
    {
        "current_password": "OldPass123!",
        "new_password": "NewPass456!"
    }
    """
    try:
        if current_user not in users_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'User not found'
            }), 404
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Validation
        if not current_password or not new_password:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'current_password and new_password required'
            }), 422
        
        if current_password == new_password:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'New password must be different from current password'
            }), 422
        
        user = users_db[current_user]
        
        # Verify current password
        if not AuthenticationUtil.verify_password(current_password, user['password']):
            logger.warning(f'Password change failed for user {current_user}: invalid current password')
            return jsonify({
                'error': 'AUTHENTICATION_ERROR',
                'message': 'Invalid current password'
            }), 401
        
        # Validate new password
        is_valid, msg = ValidationUtil.validate_password(new_password)
        if not is_valid:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': msg
            }), 422
        
        # Update password
        user['password'] = AuthenticationUtil.hash_password(new_password)
        
        log_audit_event('PASSWORD_CHANGED', current_user, 'password', {})
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
    
    except Exception as e:
        logger.error(f'Error changing password: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to change password'
        }), 500

@bp.route('/<user_email>', methods=['GET'])
@require_auth
def get_user(current_user, user_email):
    """
    Get user by email (admin only)
    
    GET /api/users/user@example.com
    Headers: Authorization: Bearer <token>
    """
    try:
        # Check admin role
        if current_user not in users_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'User not found'
            }), 404
        
        if 'admin' not in users_db[current_user].get('roles', []):
            return jsonify({
                'error': 'FORBIDDEN',
                'message': 'Admin role required'
            }), 403
        
        if user_email not in users_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'User not found'
            }), 404
        
        user = users_db[user_email]
        
        user_data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'roles': user['roles'],
            'created_at': user.get('created_at')
        }
        
        return jsonify({
            'data': user_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching user {user_email}: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to fetch user'
        }), 500
