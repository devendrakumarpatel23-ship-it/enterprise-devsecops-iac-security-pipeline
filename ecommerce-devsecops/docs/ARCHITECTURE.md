# Architecture & Design

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React Frontend (Port 3000)                          │   │
│  │  - SPA with Redux state management                   │   │
│  │  - Secure API client with JWT auth                  │   │
│  │  - CSP headers & XSS protection                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓↑
        ┌─────────────────────────────────┐
        │   API Gateway / Load Balancer   │
        │   - TLS/SSL Termination        │
        │   - Rate Limiting              │
        │   - DDoS Protection            │
        └─────────────────────────────────┘
                          ↓↑
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Flask Backend (Port 5000)                           │   │
│  │  - RESTful API endpoints                             │   │
│  │  - JWT-based authentication                          │   │
│  │  - RBAC (Role-Based Access Control)                 │   │
│  │  - Input validation & sanitization                   │   │
│  │  - Security middleware                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓↑
┌─────────────────────────────────────────────────────────────┐
│                  Data Layer                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  MongoDB (Port 27017)                                │   │
│  │  - Document-based database                           │   │
│  │  - Encrypted at rest                                 │   │
│  │  - Automated backups                                 │   │
│  │  - Access control lists                              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Redis Cache (Port 6379)                             │   │
│  │  - Session management                                │   │
│  │  - Rate limit counters                               │   │
│  │  - Distributed caching                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓↑
┌─────────────────────────────────────────────────────────────┐
│              Observability & Security Layer                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Prometheus (Port 9090) - Metrics Aggregation        │   │
│  │  Grafana (Port 3001) - Visualization                 │   │
│  │  ELK Stack - Log Aggregation & Analysis              │   │
│  │  SonarQube (Port 9000) - Code Quality                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🔐 Security Architecture

### Defense in Depth Strategy

1. **Perimeter Security**
   - WAF rules for common attacks
   - DDoS protection
   - Rate limiting

2. **Authentication & Authorization**
   - JWT tokens with expiration
   - OAuth2 support
   - MFA ready
   - RBAC implementation

3. **Data Protection**
   - Encryption in transit (TLS 1.3)
   - Encryption at rest (AES-256)
   - Field-level encryption for PII

4. **Input/Output Validation**
   - Input sanitization
   - Output encoding
   - SQL injection prevention
   - XSS protection

5. **Logging & Monitoring**
   - Centralized logging
   - Real-time alerting
   - Audit trails
   - Security event detection

## 📦 Technology Stack

### Backend
- **Framework:** Flask 2.3+
- **Database:** MongoDB
- **Cache:** Redis
- **Authentication:** JWT, OAuth2
- **ORM:** PyMongo
- **Testing:** pytest

### Frontend
- **Framework:** React 18+
- **State:** Redux Toolkit
- **Styling:** CSS Modules
- **HTTP:** Axios
- **Testing:** Jest, React Testing Library

### DevOps
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (EKS)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Registry:** ECR, GHCR

### Security
- **SAST:** Semgrep, SonarQube
- **SCA:** Snyk, npm audit
- **IaC:** Checkov
- **Container:** Trivy
- **DAST:** OWASP ZAP
- **Secrets:** GitLeaks, GitHub Secrets

### Observability
- **Metrics:** Prometheus
- **Visualization:** Grafana
- **Logging:** ELK Stack
- **Tracing:** Jaeger (optional)

## 🔄 API Design

### RESTful Principles
- Resource-oriented URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Proper status codes
- JSON responses

### API Versioning
- URL-based: `/api/v1/...`
- Header-based: `Accept: application/json;version=1`

### Error Handling
- Consistent error format
- Appropriate HTTP status codes
- Detailed error messages
- Request IDs for tracking

### Rate Limiting
- Per IP: 200 requests/day, 50/hour
- Per user: 1000 requests/day
- Per endpoint: Variable based on sensitivity

## 🌐 Deployment Architecture

### Development
- Docker Compose for local development
- All services in single network
- Shared volumes for code

### Staging
- Kubernetes cluster
- Separate namespaces
- External database
- Load balancer

### Production
- Multi-AZ Kubernetes cluster
- RDS managed database
- CloudFront CDN
- Auto-scaling groups
- Automated backups

## 📊 Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password_hash": "bcrypt_hash",
  "first_name": "John",
  "last_name": "Doe",
  "roles": ["user"],
  "created_at": timestamp,
  "updated_at": timestamp,
  "last_login": timestamp
}
```

### Products Collection
```json
{
  "_id": ObjectId,
  "name": "Product Name",
  "description": "Description",
  "price": 99.99,
  "stock": 100,
  "category": "Electronics",
  "rating": 4.5,
  "created_at": timestamp
}
```

### Orders Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "items": [{
    "product_id": ObjectId,
    "quantity": 2,
    "price": 99.99
  }],
  "total": 199.98,
  "status": "pending",
  "shipping_address": {},
  "payment_method": "credit_card",
  "created_at": timestamp,
  "updated_at": timestamp
}
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh
- `GET /api/auth/verify` - Token verification

### Products
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Orders
- `GET /api/orders` - User's orders
- `GET /api/orders/{id}` - Get order
- `POST /api/orders` - Create order
- `POST /api/orders/{id}/cancel` - Cancel order

### Users
- `GET /api/users/profile` - Get profile
- `PUT /api/users/profile` - Update profile
- `PUT /api/users/password` - Change password

---

**For deployment details, see [DEPLOYMENT.md](DEPLOYMENT.md)**
