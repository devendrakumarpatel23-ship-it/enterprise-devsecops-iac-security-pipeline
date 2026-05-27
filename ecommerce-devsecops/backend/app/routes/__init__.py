"""Routes Module - API Blueprint Registration"""

# Import route blueprints
from . import auth_routes
from . import product_routes
from . import order_routes
from . import user_routes
from . import soc_api

__all__ = [
    'auth_routes',
    'product_routes',
    'order_routes',
    'user_routes',
    'soc_api',
]
