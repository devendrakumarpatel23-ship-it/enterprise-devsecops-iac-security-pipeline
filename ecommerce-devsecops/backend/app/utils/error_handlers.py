from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API Error"""
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or 'API_ERROR'

class ValidationError(APIError):
    """Validation Error"""
    def __init__(self, message, status_code=422):
        super().__init__(message, status_code, 'VALIDATION_ERROR')

class AuthenticationError(APIError):
    """Authentication Error"""
    def __init__(self, message, status_code=401):
        super().__init__(message, status_code, 'AUTHENTICATION_ERROR')

class AuthorizationError(APIError):
    """Authorization Error"""
    def __init__(self, message, status_code=403):
        super().__init__(message, status_code, 'AUTHORIZATION_ERROR')

class NotFoundError(APIError):
    """Not Found Error"""
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code, 'NOT_FOUND')

class ConflictError(APIError):
    """Conflict Error"""
    def __init__(self, message, status_code=409):
        super().__init__(message, status_code, 'CONFLICT')

class RateLimitError(APIError):
    """Rate Limit Error"""
    def __init__(self, message, status_code=429):
        super().__init__(message, status_code, 'RATE_LIMIT_EXCEEDED')

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        logger.warning(f'{error.error_code}: {error.message}')
        return jsonify({
            'error': error.error_code,
            'message': error.message,
            'status': error.status_code
        }), error.status_code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        logger.warning(f'Validation error: {error.message}')
        return jsonify({
            'error': 'VALIDATION_ERROR',
            'message': error.message,
            'status': 422
        }), 422
    
    @app.errorhandler(AuthenticationError)
    def handle_auth_error(error):
        logger.warning(f'Authentication error: {error.message}')
        return jsonify({
            'error': 'AUTHENTICATION_ERROR',
            'message': error.message,
            'status': 401
        }), 401
    
    @app.errorhandler(AuthorizationError)
    def handle_authz_error(error):
        logger.warning(f'Authorization error: {error.message}')
        return jsonify({
            'error': 'AUTHORIZATION_ERROR',
            'message': error.message,
            'status': 403
        }), 403
    
    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return jsonify({
            'error': 'NOT_FOUND',
            'message': error.message,
            'status': 404
        }), 404
    
    @app.errorhandler(ConflictError)
    def handle_conflict(error):
        logger.warning(f'Conflict: {error.message}')
        return jsonify({
            'error': 'CONFLICT',
            'message': error.message,
            'status': 409
        }), 409
    
    @app.errorhandler(RateLimitError)
    def handle_rate_limit(error):
        logger.warning(f'Rate limit exceeded: {error.message}')
        return jsonify({
            'error': 'RATE_LIMIT_EXCEEDED',
            'message': error.message,
            'status': 429
        }), 429
    
    @app.errorhandler(Exception)
    def handle_general_error(error):
        logger.error(f'Unhandled exception: {str(error)}', exc_info=True)
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'An unexpected error occurred',
            'status': 500
        }), 500
