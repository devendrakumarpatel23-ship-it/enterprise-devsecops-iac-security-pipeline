# API Documentation

## 📚 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Overview

The Enterprise DevSecOps E-commerce API is a RESTful API built with Flask. All responses are JSON-formatted.

### Base URL
```
Development:  http://localhost:5000/api
Production:   https://api.ecommerce.example.com/api
```

### API Version
```
Current: v1
```

### Response Format
```json
{
  "success": true,
  "status": 200,
  "message": "Request successful",
  "data": {},
  "timestamp": "2024-05-15T10:30:00Z"
}
```

## Authentication

### JWT Token-Based Authentication

All protected endpoints require a JWT token in the Authorization header.

#### Token Format
```
Authorization: Bearer <token>
```

#### Token Properties
- **Expiration:** 1 hour
- **Refresh Window:** 30 days
- **Algorithm:** HS256
- **Signing:** HMAC with SECRET_KEY

#### Token Refresh
Tokens can be refreshed before expiration using the refresh endpoint.

---

## Endpoints

### 🔐 Authentication Endpoints

#### Register User
Create a new user account.

```
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Request Parameters:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | ✓ | Valid email format, unique |
| password | string | ✓ | Min 12 chars, upper/lower/digit/special |
| first_name | string | ✓ | Min 2 chars, max 50 chars |
| last_name | string | ✓ | Min 2 chars, max 50 chars |

**Success Response (201):**
```json
{
  "success": true,
  "status": 201,
  "message": "User registered successfully",
  "data": {
    "user_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-05-15T10:30:00Z"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "status": 400,
  "message": "Invalid email format",
  "errors": {
    "email": "Please provide a valid email address"
  }
}
```

#### Login User
Authenticate and receive JWT token.

```
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "user_id": "507f1f77bcf86cd799439011",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user"
    }
  }
}
```

#### Refresh Token
Get a new access token using refresh token.

```
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Token refreshed successfully",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

#### Verify Token
Verify if token is valid.

```
GET /api/auth/verify
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Token is valid",
  "data": {
    "valid": true,
    "user_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "exp": 1715767800
  }
}
```

---

### 📦 Product Endpoints

#### List Products
Get paginated list of products.

```
GET /api/products?page=1&limit=10&category=electronics&sort=name
```

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | int | ✗ | 1 | Page number (1-indexed) |
| limit | int | ✗ | 10 | Items per page (max 100) |
| category | string | ✗ | - | Filter by category |
| sort | string | ✗ | created_at | Sort field (name, price, created_at) |
| order | string | ✗ | asc | Sort order (asc, desc) |

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Products retrieved successfully",
  "data": {
    "products": [
      {
        "product_id": "507f1f77bcf86cd799439011",
        "name": "Laptop",
        "description": "High-performance laptop",
        "category": "electronics",
        "price": 999.99,
        "stock": 50,
        "created_at": "2024-05-15T10:30:00Z",
        "updated_at": "2024-05-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 45,
      "pages": 5
    }
  }
}
```

#### Get Single Product
Get details of a specific product.

```
GET /api/products/{product_id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| product_id | string | ✓ | MongoDB ObjectId |

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Product retrieved successfully",
  "data": {
    "product_id": "507f1f77bcf86cd799439011",
    "name": "Laptop",
    "description": "High-performance laptop",
    "category": "electronics",
    "price": 999.99,
    "stock": 50,
    "specifications": {
      "cpu": "Intel i7",
      "ram": "16GB",
      "storage": "512GB SSD"
    },
    "created_at": "2024-05-15T10:30:00Z",
    "updated_at": "2024-05-15T10:30:00Z"
  }
}
```

#### Create Product
Create a new product (admin only).

```
POST /api/products
Authorization: Bearer <admin_token>
```

**Request Body:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "category": "electronics",
  "price": 999.99,
  "stock": 50,
  "specifications": {
    "cpu": "Intel i7",
    "ram": "16GB",
    "storage": "512GB SSD"
  }
}
```

**Success Response (201):**
```json
{
  "success": true,
  "status": 201,
  "message": "Product created successfully",
  "data": {
    "product_id": "507f1f77bcf86cd799439011",
    "name": "Laptop",
    "price": 999.99
  }
}
```

#### Update Product
Update an existing product (admin only).

```
PUT /api/products/{product_id}
Authorization: Bearer <admin_token>
```

**Request Body:**
```json
{
  "price": 899.99,
  "stock": 40
}
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Product updated successfully",
  "data": {
    "product_id": "507f1f77bcf86cd799439011",
    "name": "Laptop",
    "price": 899.99,
    "stock": 40
  }
}
```

#### Delete Product
Delete a product (admin only).

```
DELETE /api/products/{product_id}
Authorization: Bearer <admin_token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Product deleted successfully"
}
```

---

### 📋 Order Endpoints

#### Get User Orders
Get all orders for the authenticated user.

```
GET /api/orders?page=1&limit=10
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Orders retrieved successfully",
  "data": {
    "orders": [
      {
        "order_id": "507f1f77bcf86cd799439011",
        "user_id": "507f1f77bcf86cd799439012",
        "items": [
          {
            "product_id": "507f1f77bcf86cd799439013",
            "name": "Laptop",
            "price": 999.99,
            "quantity": 1
          }
        ],
        "total": 999.99,
        "status": "completed",
        "created_at": "2024-05-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 5,
      "pages": 1
    }
  }
}
```

#### Get Single Order
Get details of a specific order.

```
GET /api/orders/{order_id}
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Order retrieved successfully",
  "data": {
    "order_id": "507f1f77bcf86cd799439011",
    "user_id": "507f1f77bcf86cd799439012",
    "items": [
      {
        "product_id": "507f1f77bcf86cd799439013",
        "name": "Laptop",
        "price": 999.99,
        "quantity": 1
      }
    ],
    "total": 999.99,
    "status": "completed",
    "shipping_address": "123 Main St, City, State 12345",
    "created_at": "2024-05-15T10:30:00Z",
    "updated_at": "2024-05-15T10:30:00Z"
  }
}
```

#### Create Order
Create a new order.

```
POST /api/orders
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "items": [
    {
      "product_id": "507f1f77bcf86cd799439013",
      "quantity": 1
    }
  ],
  "shipping_address": "123 Main St, City, State 12345"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "status": 201,
  "message": "Order created successfully",
  "data": {
    "order_id": "507f1f77bcf86cd799439011",
    "total": 999.99,
    "status": "pending"
  }
}
```

#### Cancel Order
Cancel a pending order.

```
POST /api/orders/{order_id}/cancel
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Order cancelled successfully",
  "data": {
    "order_id": "507f1f77bcf86cd799439011",
    "status": "cancelled"
  }
}
```

---

### 👤 User Endpoints

#### Get User Profile
Get authenticated user's profile.

```
GET /api/users/profile
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Profile retrieved successfully",
  "data": {
    "user_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "created_at": "2024-05-15T10:30:00Z"
  }
}
```

#### Update User Profile
Update user profile information.

```
PUT /api/users/profile
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Profile updated successfully",
  "data": {
    "user_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### Change Password
Change user password.

```
PUT /api/users/password
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewPass456!",
  "confirm_password": "NewPass456!"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "status": 200,
  "message": "Password changed successfully"
}
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "success": false,
  "status": 400,
  "message": "Invalid request",
  "errors": {
    "field_name": "Error message"
  }
}
```

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate email |
| 422 | Validation Failed | Invalid data |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal server error |

### Error Codes

| Error Code | HTTP Status | Description |
|-----------|------------|-------------|
| AUTH_REQUIRED | 401 | Authentication required |
| INVALID_TOKEN | 401 | Token is invalid/expired |
| INSUFFICIENT_PERMISSIONS | 403 | User lacks permissions |
| RESOURCE_NOT_FOUND | 404 | Resource doesn't exist |
| VALIDATION_FAILED | 422 | Validation failed |
| DUPLICATE_EMAIL | 409 | Email already exists |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Internal server error |

---

## Rate Limiting

API requests are rate limited per IP address.

### Rate Limits

- **Unauthenticated:** 100 requests/day, 50 requests/hour
- **Authenticated:** 200 requests/day, 100 requests/hour
- **Admin:** 1000 requests/day, 500 requests/hour

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1715867400
```

### Rate Limit Response (429)

```json
{
  "success": false,
  "status": 429,
  "message": "Too many requests",
  "data": {
    "retry_after": 3600
  }
}
```

---

## Examples

### cURL Examples

#### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

#### Get Products (with token)
```bash
curl -X GET http://localhost:5000/api/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### JavaScript/Fetch Examples

#### Login
```javascript
const response = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123!'
  })
});

const data = await response.json();
const token = data.data.access_token;
```

#### Get Products
```javascript
const response = await fetch('http://localhost:5000/api/products', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
```

---

## SDKs & Libraries

### JavaScript
```bash
npm install ecommerce-sdk
```

### Python
```bash
pip install ecommerce-sdk
```

---

## Support & Feedback

- **Issues:** [GitHub Issues](https://github.com/yourorg/ecommerce-devsecops/issues)
- **Security:** [SECURITY.md](../SECURITY.md)
- **Documentation:** [docs/](../)

---

**API Version:** 1.0.0  
**Last Updated:** May 2024  
**Status:** ✅ Production Ready
