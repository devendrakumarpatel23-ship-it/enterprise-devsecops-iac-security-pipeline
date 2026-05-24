import pytest
from app import app as flask_app
import json

@pytest.fixture
def app():
    """Create application for testing"""
    flask_app.config['TESTING'] = True
    flask_app.config['ENV'] = 'testing'
    return flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

class TestAuth:
    """Authentication endpoint tests"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register', 
            json={
                'email': 'newuser@example.com',
                'password': 'SecurePass123!',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User registered successfully'
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        response = client.post('/api/auth/register',
            json={
                'email': 'newuser@example.com',
                'password': 'SecurePass123!'
            },
            content_type='application/json'
        )
        assert response.status_code == 422
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/api/auth/register',
            json={
                'email': 'invalid-email',
                'password': 'SecurePass123!',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            content_type='application/json'
        )
        assert response.status_code == 422
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register',
            json={
                'email': 'user@example.com',
                'password': 'weak',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            content_type='application/json'
        )
        assert response.status_code == 422

class TestProducts:
    """Product endpoint tests"""
    
    def test_get_products(self, client):
        """Test getting all products"""
        response = client.get('/api/products')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert 'pagination' in data
    
    def test_get_products_with_pagination(self, client):
        """Test products with pagination"""
        response = client.get('/api/products?page=1&limit=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pagination']['page'] == 1
        assert data['pagination']['limit'] == 5
    
    def test_get_product_by_id(self, client):
        """Test getting single product"""
        response = client.get('/api/products/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert data['data']['id'] == '1'
    
    def test_get_nonexistent_product(self, client):
        """Test getting non-existent product"""
        response = client.get('/api/products/99999')
        assert response.status_code == 404

class TestHealthCheck:
    """Health check endpoint tests"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_index(self, client):
        """Test root endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
