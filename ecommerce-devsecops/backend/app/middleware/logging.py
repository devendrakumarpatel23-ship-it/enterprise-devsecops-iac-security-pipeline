import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logging(app):
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # File handler for all logs
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # File handler for security logs
    security_handler = RotatingFileHandler(
        'logs/security.log',
        maxBytes=10485760,  # 10MB
        backupCount=20
    )
    
    # File handler for audit logs
    audit_handler = RotatingFileHandler(
        'logs/audit.log',
        maxBytes=10485760,  # 10MB
        backupCount=30
    )
    
    # Log formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    security_handler.setFormatter(formatter)
    audit_handler.setFormatter(formatter)
    
    # Set log level
    log_level = logging.DEBUG if app.config['ENV'] == 'development' else logging.INFO
    file_handler.setLevel(log_level)
    security_handler.setLevel(logging.WARNING)
    audit_handler.setLevel(logging.INFO)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(security_handler)
    app.logger.addHandler(audit_handler)
    
    # Set app logger level
    app.logger.setLevel(log_level)
    
    # Log startup
    app.logger.info(f'Application started in {app.config["ENV"]} mode')

def log_security_event(event_type, user_id, details, severity='INFO'):
    """Log security-related events"""
    logger = logging.getLogger('security')
    message = f'[{event_type}] User: {user_id} | Details: {details}'
    
    if severity == 'CRITICAL':
        logger.critical(message)
    elif severity == 'ERROR':
        logger.error(message)
    elif severity == 'WARNING':
        logger.warning(message)
    else:
        logger.info(message)

def log_audit_event(action, user_id, resource, changes):
    """Log audit trail events"""
    logger = logging.getLogger('audit')
    message = f'[{action}] User: {user_id} | Resource: {resource} | Changes: {changes}'
    logger.info(message)
