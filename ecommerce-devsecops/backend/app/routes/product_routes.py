from flask import Blueprint, request, jsonify
from app.middleware.security import require_auth, validate_json_request
from app.middleware.logging import log_audit_event
import logging

bp = Blueprint('products', __name__, url_prefix='/api/products')
logger = logging.getLogger(__name__)

# Mock product database
products_db = {
    '1': {
        'id': '1',
        'name': 'Laptop',
        'description': 'High-performance laptop',
        'price': 999.99,
        'stock': 50,
        'category': 'Electronics',
        'rating': 4.5
    },
    '2': {
        'id': '2',
        'name': 'Smartphone',
        'description': 'Latest smartphone',
        'price': 799.99,
        'stock': 100,
        'category': 'Electronics',
        'rating': 4.7
    }
}

@bp.route('', methods=['GET'])
def get_products():
    """
    Get all products with pagination and filtering
    
    GET /api/products?page=1&limit=10&category=Electronics
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        category = request.args.get('category', '', type=str)
        
        # Validation
        if page < 1 or limit < 1:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Invalid page or limit'
            }), 422
        
        # Filter products
        filtered_products = [
            p for p in products_db.values()
            if not category or p['category'].lower() == category.lower()
        ]
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_products = filtered_products[start:end]
        
        return jsonify({
            'data': paginated_products,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': len(filtered_products),
                'pages': (len(filtered_products) + limit - 1) // limit
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching products: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to fetch products'
        }), 500

@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get single product by ID
    
    GET /api/products/1
    """
    try:
        if product_id not in products_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'Product not found'
            }), 404
        
        product = products_db[product_id]
        return jsonify({
            'data': product
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching product {product_id}: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to fetch product'
        }), 500

@bp.route('', methods=['POST'])
@require_auth
@validate_json_request
def create_product(current_user, data):
    """
    Create new product (admin only)
    
    POST /api/products
    {
        "name": "Product Name",
        "description": "Product description",
        "price": 99.99,
        "stock": 100,
        "category": "Category"
    }
    """
    try:
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = data.get('price')
        stock = data.get('stock')
        category = data.get('category', '').strip()
        
        # Validation
        if not all([name, description, price, category]):
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Missing required fields'
            }), 422
        
        if not isinstance(price, (int, float)) or price < 0:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Invalid price'
            }), 422
        
        if not isinstance(stock, int) or stock < 0:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Invalid stock'
            }), 422
        
        # Create product
        product_id = str(max(int(pid) for pid in products_db.keys() if pid.isdigit()) + 1)
        product = {
            'id': product_id,
            'name': name,
            'description': description,
            'price': price,
            'stock': stock,
            'category': category,
            'rating': 0
        }
        
        products_db[product_id] = product
        
        log_audit_event('PRODUCT_CREATED', current_user, f'product:{product_id}', {'name': name, 'price': price})
        
        return jsonify({
            'message': 'Product created successfully',
            'data': product
        }), 201
    
    except Exception as e:
        logger.error(f'Error creating product: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to create product'
        }), 500

@bp.route('/<product_id>', methods=['PUT'])
@require_auth
@validate_json_request
def update_product(current_user, product_id, data):
    """
    Update product (admin only)
    
    PUT /api/products/1
    {
        "name": "Updated Name",
        "price": 199.99,
        "stock": 75
    }
    """
    try:
        if product_id not in products_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'Product not found'
            }), 404
        
        product = products_db[product_id]
        
        # Update fields
        if 'name' in data:
            product['name'] = data['name'].strip()
        if 'description' in data:
            product['description'] = data['description'].strip()
        if 'price' in data:
            if data['price'] < 0:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Price cannot be negative'
                }), 422
            product['price'] = data['price']
        if 'stock' in data:
            if data['stock'] < 0:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Stock cannot be negative'
                }), 422
            product['stock'] = data['stock']
        if 'category' in data:
            product['category'] = data['category'].strip()
        
        log_audit_event('PRODUCT_UPDATED', current_user, f'product:{product_id}', data)
        
        return jsonify({
            'message': 'Product updated successfully',
            'data': product
        }), 200
    
    except Exception as e:
        logger.error(f'Error updating product {product_id}: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to update product'
        }), 500

@bp.route('/<product_id>', methods=['DELETE'])
@require_auth
def delete_product(current_user, product_id):
    """
    Delete product (admin only)
    
    DELETE /api/products/1
    """
    try:
        if product_id not in products_db:
            return jsonify({
                'error': 'NOT_FOUND',
                'message': 'Product not found'
            }), 404
        
        del products_db[product_id]
        
        log_audit_event('PRODUCT_DELETED', current_user, f'product:{product_id}', {})
        
        return jsonify({
            'message': 'Product deleted successfully'
        }), 200
    
    except Exception as e:
        logger.error(f'Error deleting product {product_id}: {str(e)}')
        return jsonify({
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Failed to delete product'
        }), 500
