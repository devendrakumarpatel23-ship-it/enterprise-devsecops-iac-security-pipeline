# Deployment Guide

## 📋 Prerequisites

### Required Tools
- Docker & Docker Compose 20.10+
- Python 3.9+
- Node.js 16+
- Terraform 1.0+
- kubectl 1.25+
- AWS CLI v2
- Git

### AWS Account Requirements
- EKS cluster permissions
- RDS permissions
- CloudFormation permissions
- VPC/Network permissions
- IAM permissions

## 🚀 Local Development Deployment

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourorg/ecommerce-devsecops.git
cd ecommerce-devsecops

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit .env files with your values
nano backend/.env
nano frontend/.env
```

### 2. Start Services with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 3. Verify Services

```bash
# Backend health check
curl http://localhost:5000/health

# Frontend
open http://localhost:3000

# Prometheus
open http://localhost:9090

# Grafana
open http://localhost:3001
# Default credentials: admin/admin

# SonarQube
open http://localhost:9000
# Default credentials: admin/admin
```

## 🌍 AWS Deployment (EKS)

### 1. Setup AWS Infrastructure with Terraform

```bash
cd infrastructure/terraform/environments/dev

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply infrastructure
terraform apply
```

### 2. Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig \
  --name ecommerce-cluster-dev \
  --region us-east-1

# Verify connection
kubectl cluster-info
kubectl get nodes
```

### 3. Create Kubernetes Secrets

```bash
# Create namespace
kubectl create namespace ecommerce

# Create secrets
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=$DB_PASSWORD \
  -n ecommerce

kubectl create secret generic app-secrets \
  --from-literal=jwt-secret-key=$JWT_SECRET \
  --from-literal=encryption-key=$ENCRYPTION_KEY \
  -n ecommerce
```

### 4. Deploy Application

```bash
# Build and push Docker images
docker build -t ghcr.io/yourorg/backend:latest ./backend
docker build -t ghcr.io/yourorg/frontend:latest ./frontend

docker push ghcr.io/yourorg/backend:latest
docker push ghcr.io/yourorg/frontend:latest

# Deploy using kubectl or Helm
kubectl apply -f deployment.yaml -n ecommerce

# Verify deployment
kubectl get pods -n ecommerce
kubectl get services -n ecommerce
```

## 🔐 Security Configuration

### 1. Enable TLS

```bash
# Create TLS secret
kubectl create secret tls app-tls \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem \
  -n ecommerce
```

### 2. Setup Network Policies

```bash
# Apply network policies
kubectl apply -f network-policies.yaml -n ecommerce
```

### 3. Configure RBAC

```bash
# Create roles
kubectl apply -f rbac.yaml -n ecommerce
```

## 📊 Monitoring Setup

### 1. Deploy Prometheus

```bash
# Using Helm
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --create-namespace
```

### 2. Configure Grafana

- Access: http://your-domain:3001
- Add Prometheus data source
- Import dashboards
- Setup alert notifications

## 🔄 CI/CD Pipeline Setup

### 1. GitHub Actions Secrets

```bash
# Add these secrets to your GitHub repository
SONAR_HOST_URL=https://your-sonarqube.com
SONAR_TOKEN=your-token
SNYK_TOKEN=your-token
REGISTRY_USERNAME=your-username
REGISTRY_PASSWORD=your-password
```

### 2. Enable Branch Protection

- Require PR reviews (2 minimum)
- Require status checks to pass
- Require branches to be up to date
- Dismiss stale reviews
- Restrict who can push

## 🗄️ Database Migrations

### 1. MongoDB Initialization

```bash
# Connect to MongoDB
mongosh mongodb://admin:password@localhost:27017/ecommerce

# Create indexes
db.users.createIndex({ email: 1 }, { unique: true })
db.products.createIndex({ category: 1 })
db.orders.createIndex({ user_id: 1, created_at: -1 })
```

### 2. Data Seeding

```bash
# Load sample data
python scripts/seed_database.py
```

## 🔧 Configuration Management

### 1. Environment Specific Configs

```
config/
├── development.py
├── staging.py
├── production.py
└── common.py
```

### 2. Feature Flags

```python
# Feature flag management
FEATURES = {
    'new_checkout': True,
    'ai_scoring': False,
    'advanced_analytics': True
}
```

## 📈 Scaling & Performance

### 1. Auto-scaling

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 2. Load Testing

```bash
# Using Apache Bench
ab -n 10000 -c 100 http://your-api.com/api/products
```

## 🔄 Backup & Recovery

### 1. Database Backups

```bash
# MongoDB backup
mongodump --uri="mongodb://admin:pass@localhost:27017/ecommerce" \
  --out=./backups/mongo-$(date +%Y%m%d)

# Restore
mongorestore --uri="mongodb://admin:pass@localhost:27017" \
  ./backups/mongo-20240101
```

### 2. AWS RDS Backups

```bash
# Enable automated backups (Terraform)
enable_backup          = true
backup_retention_days  = 30
```

## 🧪 Health Checks

### 1. Application Health

```bash
# Backend health
curl -s http://localhost:5000/health | jq .

# Database connectivity
curl -s http://localhost:5000/api/health/db | jq .
```

### 2. Kubernetes Health

```bash
# Check pod health
kubectl get pods -n ecommerce

# Check service endpoints
kubectl get endpoints -n ecommerce
```

## 📝 Logs & Troubleshooting

### 1. Docker Logs

```bash
# View logs
docker-compose logs -f backend

# Filter logs
docker-compose logs backend | grep ERROR
```

### 2. Kubernetes Logs

```bash
# View pod logs
kubectl logs -f deployment/backend -n ecommerce

# View previous logs
kubectl logs -p deployment/backend -n ecommerce
```

### 3. Common Issues

**Issue:** Database connection refused
```bash
# Check database service
kubectl get svc -n ecommerce
# Verify connection string
kubectl exec -it deployment/backend -n ecommerce -- \
  python -c "from app import app; print(app.config['MONGODB_URI'])"
```

**Issue:** Out of memory
```bash
# Check resource usage
kubectl top pods -n ecommerce
# Increase resource limits
kubectl set resources deployment backend \
  --limits=memory=2Gi,cpu=1000m \
  -n ecommerce
```

## 🚢 Deployment Checklist

- [ ] Environment variables configured
- [ ] Secrets created
- [ ] Database migrated
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Logs aggregated
- [ ] Backups enabled
- [ ] SSL/TLS certificates installed
- [ ] DNS records updated
- [ ] Smoke tests passed
- [ ] Security scan completed
- [ ] Performance baseline established

---

For more information, see [ARCHITECTURE.md](ARCHITECTURE.md) and [SECURITY.md](SECURITY.md)
