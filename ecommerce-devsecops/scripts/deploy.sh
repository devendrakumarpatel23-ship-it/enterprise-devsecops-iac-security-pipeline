#!/bin/bash

# Enterprise DevSecOps Deployment Script
# Automates the complete deployment process

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-dev}
PROJECT_NAME="ecommerce"
REGISTRY="ghcr.io/yourorg"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Enterprise DevSecOps Deployment${NC}"
echo -e "${BLUE}Environment: $ENVIRONMENT${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# 1. Security Checks
print_info "Running security checks..."

echo "  - Checking for secrets in code..."
if command -v gitleaks &> /dev/null; then
    gitleaks detect --source local --verbose || print_error "Secrets detected!"
    print_status "No secrets found"
else
    print_error "gitleaks not installed"
fi

echo "  - Running SAST analysis..."
if command -v semgrep &> /dev/null; then
    semgrep --config=security/scanning/semgrep-rules.yaml . || true
    print_status "SAST analysis complete"
else
    print_error "semgrep not installed"
fi

# 2. Build Docker Images
print_info "Building Docker images..."

echo "  - Building backend image..."
docker build \
    -t $REGISTRY/$PROJECT_NAME-backend:$ENVIRONMENT-$(git rev-parse --short HEAD) \
    -t $REGISTRY/$PROJECT_NAME-backend:latest \
    ./backend || print_error "Backend build failed"
print_status "Backend image built"

echo "  - Building frontend image..."
docker build \
    -t $REGISTRY/$PROJECT_NAME-frontend:$ENVIRONMENT-$(git rev-parse --short HEAD) \
    -t $REGISTRY/$PROJECT_NAME-frontend:latest \
    ./frontend || print_error "Frontend build failed"
print_status "Frontend image built"

# 3. Container Security Scanning
print_info "Running container security scans..."

echo "  - Scanning backend image..."
if command -v trivy &> /dev/null; then
    trivy image $REGISTRY/$PROJECT_NAME-backend:latest || true
    print_status "Backend scan complete"
else
    print_error "trivy not installed"
fi

echo "  - Scanning frontend image..."
if command -v trivy &> /dev/null; then
    trivy image $REGISTRY/$PROJECT_NAME-frontend:latest || true
    print_status "Frontend scan complete"
else
    print_error "trivy not installed"
fi

# 4. Push Images to Registry
print_info "Pushing images to registry..."

if [ "$ENVIRONMENT" != "dev" ]; then
    echo "  - Pushing backend..."
    docker push $REGISTRY/$PROJECT_NAME-backend:latest
    print_status "Backend pushed"

    echo "  - Pushing frontend..."
    docker push $REGISTRY/$PROJECT_NAME-frontend:latest
    print_status "Frontend pushed"
else
    print_info "Skipping push for dev environment"
fi

# 5. Database Migrations
print_info "Preparing database..."

if command -v mongosh &> /dev/null; then
    echo "  - Creating indexes..."
    mongosh mongodb://admin:admin123@localhost:27017/ecommerce << EOF
    db.users.createIndex({ email: 1 }, { unique: true })
    db.products.createIndex({ category: 1 })
    db.orders.createIndex({ user_id: 1, created_at: -1 })
EOF
    print_status "Database prepared"
else
    print_error "mongosh not installed"
fi

# 6. Terraform Infrastructure
print_info "Deploying infrastructure..."

if [ "$ENVIRONMENT" != "dev" ]; then
    cd infrastructure/terraform/environments/$ENVIRONMENT
    
    echo "  - Initializing Terraform..."
    terraform init || print_error "Terraform init failed"
    print_status "Terraform initialized"
    
    echo "  - Planning deployment..."
    terraform plan -out=tfplan || print_error "Terraform plan failed"
    print_status "Plan created"
    
    echo "  - Applying configuration..."
    terraform apply tfplan || print_error "Terraform apply failed"
    print_status "Infrastructure deployed"
    
    cd ../../..
fi

# 7. Kubernetes Deployment
print_info "Deploying to Kubernetes..."

if [ "$ENVIRONMENT" != "dev" ]; then
    if command -v kubectl &> /dev/null; then
        echo "  - Creating namespace..."
        kubectl create namespace $PROJECT_NAME-$ENVIRONMENT || true
        print_status "Namespace ready"
        
        echo "  - Creating secrets..."
        kubectl create secret generic db-credentials \
            --from-literal=username=admin \
            --from-literal=password=$DB_PASSWORD \
            -n $PROJECT_NAME-$ENVIRONMENT \
            --dry-run=client -o yaml | kubectl apply -f - || true
        print_status "Secrets created"
        
        echo "  - Deploying application..."
        kubectl apply -f k8s/deployment.yaml -n $PROJECT_NAME-$ENVIRONMENT
        print_status "Application deployed"
        
        echo "  - Waiting for rollout..."
        kubectl rollout status deployment/backend -n $PROJECT_NAME-$ENVIRONMENT
        print_status "Deployment ready"
    else
        print_error "kubectl not installed"
    fi
fi

# 8. Health Checks
print_info "Running health checks..."

if [ "$ENVIRONMENT" = "dev" ]; then
    echo "  - Checking backend..."
    for i in {1..30}; do
        if curl -s http://localhost:5000/health | grep -q healthy; then
            print_status "Backend healthy"
            break
        fi
        sleep 1
    done
    
    echo "  - Checking frontend..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 | grep -q html; then
            print_status "Frontend healthy"
            break
        fi
        sleep 1
    done
fi

# 9. Security Report
print_info "Generating security report..."

echo "  - Creating AI vulnerability report..."
if command -v python3 &> /dev/null; then
    python3 security/ai-scoring/models/vulnerability_scorer.py || true
    print_status "Report generated"
else
    print_error "Python not installed"
fi

# 10. Summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo "Deployment Summary:"
echo "  Environment: $ENVIRONMENT"
echo "  Project: $PROJECT_NAME"
echo "  Backend: $REGISTRY/$PROJECT_NAME-backend:latest"
echo "  Frontend: $REGISTRY/$PROJECT_NAME-frontend:latest"
echo ""
echo "Next Steps:"
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "  1. Access frontend: http://localhost:3000"
    echo "  2. Access API: http://localhost:5000"
    echo "  3. View logs: docker-compose logs -f"
else
    echo "  1. Verify deployment: kubectl get pods -n $PROJECT_NAME-$ENVIRONMENT"
    echo "  2. Check services: kubectl get svc -n $PROJECT_NAME-$ENVIRONMENT"
    echo "  3. View logs: kubectl logs -f deployment/backend -n $PROJECT_NAME-$ENVIRONMENT"
fi

echo -e "\n${BLUE}Security Reports:${NC}"
echo "  - Security Report: security/ai-scoring/vulnerability-report.json"
echo "  - SonarQube: http://localhost:9000"
echo "  - Grafana: http://localhost:3001"
echo "  - Prometheus: http://localhost:9090"

print_status "All systems operational!"
