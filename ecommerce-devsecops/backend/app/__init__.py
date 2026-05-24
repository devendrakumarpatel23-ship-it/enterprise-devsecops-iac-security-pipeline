import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_jwt_extended import JWTManager
import logging
from dotenv import load_dotenv

# Import routes and middleware
from app.routes import auth_routes, product_routes, order_routes, user_routes
from app.middleware.security import SecurityMiddleware
from app.middleware.logging import setup_logging
from app.utils.error_handlers import register_error_handlers

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ecommerce')
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')

# Security Headers
Talisman(
    app,
    force_https=os.getenv('FORCE_HTTPS', 'True') == 'True',
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'font-src': "'self' data:",
        'connect-src': "'self'",
    },
    referrer_policy='strict-origin-when-cross-origin',
    permissions_policy={
        'geolocation': [],
        'microphone': [],
        'camera': [],
    }
)

# CORS Configuration
CORS(
    app,
    resources={r'/api/*': {
        'origins': os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(','),
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization'],
        'supports_credentials': True,
        'max_age': 3600
    }}
)

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=['200 per day', '50 per hour'],
    storage_uri=os.getenv('REDIS_URI', 'memory://')
)

# JWT Manager
jwt = JWTManager(app)

# Security Middleware
app.before_request(SecurityMiddleware.validate_request)

# Setup Logging
setup_logging(app)
logger = logging.getLogger(__name__)

# Register Error Handlers
register_error_handlers(app)

# Register Routes
app.register_blueprint(auth_routes.bp)
app.register_blueprint(product_routes.bp)
app.register_blueprint(order_routes.bp)
app.register_blueprint(user_routes.bp)

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'environment': app.config['ENV']
    }), 200

# Root Endpoint
@app.route('/', methods=['GET'])
def index():
    """API root endpoint"""
    return jsonify({
        'message': 'E-commerce DevSecOps API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'products': '/api/products',
            'orders': '/api/orders',
            'users': '/api/users',
            'health': '/health'
        }
    }), 200

# 404 Handler
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status': 404
    }), 404

# 500 Handler
@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Internal Server Error: {str(error)}')
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'status': 500
    }), 500

if __name__ == '__main__':
    debug_mode = app.config['ENV'] == 'development'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug_mode,
        use_reloader=debug_mode
    )
