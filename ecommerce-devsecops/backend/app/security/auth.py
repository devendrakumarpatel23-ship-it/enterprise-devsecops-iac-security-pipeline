import hashlib
import hmac
import re
import os
from datetime import datetime, timedelta
from functools import wraps
from flask_jwt_extended import create_access_token, create_refresh_token
import logging

logger = logging.getLogger(__name__)

class AuthenticationUtil:
    """Authentication utilities"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using PBKDF2"""
        import bcrypt
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def create_tokens(user_id, email, roles=['user']):
        """Create access and refresh tokens"""
        additional_claims = {
            'email': email,
            'roles': roles
        }
        
        access_token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        
        refresh_token = create_refresh_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=timedelta(days=30)
        )
        
        return access_token, refresh_token

class ValidationUtil:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength
        Requirements:
        - At least 12 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 digit
        - At least 1 special character
        """
        if len(password) < 12:
            return False, 'Password must be at least 12 characters'
        
        if not re.search(r'[A-Z]', password):
            return False, 'Password must contain uppercase letter'
        
        if not re.search(r'[a-z]', password):
            return False, 'Password must contain lowercase letter'
        
        if not re.search(r'\d', password):
            return False, 'Password must contain digit'
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, 'Password must contain special character'
        
        return True, 'Password valid'
    
    @staticmethod
    def sanitize_input(user_input):
        """Sanitize user input to prevent injection attacks"""
        # Remove null bytes
        user_input = user_input.replace('\x00', '')
        
        # Escape special characters
        special_chars = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '&': '&amp;'
        }
        
        for char, escaped in special_chars.items():
            user_input = user_input.replace(char, escaped)
        
        return user_input
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None

class EncryptionUtil:
    """Encryption utilities"""
    
    @staticmethod
    def encrypt_sensitive_data(data, key=None):
        """Encrypt sensitive data"""
        if key is None:
            key = os.getenv('ENCRYPTION_KEY', 'dev-key-change-in-production')
        
        from cryptography.fernet import Fernet
        cipher = Fernet(key.encode() if isinstance(key, str) else key)
        return cipher.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt_sensitive_data(encrypted_data, key=None):
        """Decrypt sensitive data"""
        if key is None:
            key = os.getenv('ENCRYPTION_KEY', 'dev-key-change-in-production')
        
        from cryptography.fernet import Fernet
        cipher = Fernet(key.encode() if isinstance(key, str) else key)
        return cipher.decrypt(encrypted_data.encode()).decode()

class CSRFUtil:
    """CSRF protection utilities"""
    
    @staticmethod
    def generate_csrf_token():
        """Generate CSRF token"""
        import secrets
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_csrf_token(token, session_token):
        """Validate CSRF token"""
        return hmac.compare_digest(token, session_token)
