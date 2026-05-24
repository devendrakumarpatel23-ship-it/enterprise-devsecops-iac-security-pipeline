from flask import Blueprint, request, jsonify
from app.middleware.security import require_auth, validate_json_request
from app.middleware.logging import log_audit_event
import logging
from datetime import datetime

bp = Blueprint('orders', __name__, url_prefix='/api/orders')
logger = logging.getLogger(__name__)

# Mock order database
orders_db = {}
order_counter = 0

@bp.route('', methods=['GET'])
@require_auth
def get_orders(current_user):
    """
    Get user's orders
    
    GET /api/orders
    Headers: Authorization: Bearer <token>
    """
    try:
        user_orders = [
            order for order in orders_db.values()
            if order['user_id'] == current_user
        ]
        
        return jsonify({
            'data': user_orders,
            'count': len(user_orders)
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching orders: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to fetch orders'
        }), 500

@bp.route('/<order_id>', methods=['GET'])
@require_auth
def get_order(current_user, order_id):
    """
    Get single order
    
    GET /api/orders/1
    Headers: Authorization: Bearer <token>
    """
    try:
        if order_id not in orders_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'Order not found'
            }), 404
        
        order = orders_db[order_id]
        
        # Check authorization
        if order['user_id'] != current_user:
            return jsonify({
                'error': 'FORBIDDEN',
                'message': 'Not authorized to view this order'
            }), 403
        
        return jsonify({
            'data': order
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching order {order_id}: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to fetch order'
        }), 500

@bp.route('', methods=['POST'])
@require_auth
@validate_json_request
def create_order(current_user, data):
    """
    Create new order
    
    POST /api/orders
    {
        "items": [
            {
                "product_id": "1",
                "quantity": 2,
                "price": 999.99
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "City",
            "state": "State",
            "zip": "12345",
            "country": "Country"
        },
        "payment_method": "credit_card"
    }
    """
    try:
        global order_counter
        
        items = data.get('items', [])
        shipping_address = data.get('shipping_address', {})
        payment_method = data.get('payment_method', '')
        
        # Validation
        if not items or not shipping_address or not payment_method:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Missing required fields: items, shipping_address, payment_method'
            }), 422
        
        if not isinstance(items, list) or len(items) == 0:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Order must contain at least one item'
            }), 422
        
        # Calculate total
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        
        if total <= 0:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Order total must be greater than zero'
            }), 422
        
        # Create order
        order_counter += 1
        order_id = str(order_counter)
        
        order = {
            'id': order_id,
            'user_id': current_user,
            'items': items,
            'total': total,
            'status': 'pending',
            'shipping_address': shipping_address,
            'payment_method': payment_method,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        orders_db[order_id] = order
        
        log_audit_event('ORDER_CREATED', current_user, f'order:{order_id}', {
            'total': total,
            'items_count': len(items)
        })
        
        return jsonify({
            'message': 'Order created successfully',
            'data': order
        }), 201
    
    except Exception as e:
        logger.error(f'Error creating order: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to create order'
        }), 500

@bp.route('/<order_id>/cancel', methods=['POST'])
@require_auth
def cancel_order(current_user, order_id):
    """
    Cancel order
    
    POST /api/orders/1/cancel
    Headers: Authorization: Bearer <token>
    """
    try:
        if order_id not in orders_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'Order not found'
            }), 404
        
        order = orders_db[order_id]
        
        # Check authorization
        if order['user_id'] != current_user:
            return jsonify({
                'error': 'FORBIDDEN',
                'message': 'Not authorized to cancel this order'
            }), 403
        
        # Check status
        if order['status'] not in ['pending', 'confirmed']:
            return jsonify({
                'error': 'CONFLICT',
                'message': f'Cannot cancel order with status: {order["status"]}'
            }), 409
        
        order['status'] = 'cancelled'
        order['updated_at'] = datetime.utcnow().isoformat()
        
        log_audit_event('ORDER_CANCELLED', current_user, f'order:{order_id}', {})
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'data': order
        }), 200
    
    except Exception as e:
        logger.error(f'Error cancelling order {order_id}: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to cancel order'
        }), 500
