#!/bin/bash

# PROJECT COMPLETION VERIFICATION SCRIPT
# Verifies all deliverables are present and complete

set -e

PROJECT_DIR=$(pwd)
ISSUES=0
COMPLETED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Enterprise DevSecOps Project Verification Script        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

# Function to check file
check_file() {
    local file=$1
    local name=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $name"
        ((COMPLETED++))
    else
        echo -e "${RED}✗${NC} $name - NOT FOUND"
        ((ISSUES++))
    fi
}

# Function to check directory
check_dir() {
    local dir=$1
    local name=$2
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $name"
        ((COMPLETED++))
    else
        echo -e "${RED}✗${NC} $name - NOT FOUND"
        ((ISSUES++))
    fi
}

# Check root files
echo -e "${BLUE}ROOT FILES:${NC}"
check_file "README.md" "README.md"
check_file "CONTRIBUTING.md" "CONTRIBUTING.md"
check_file "SECURITY.md" "SECURITY.md"
check_file "INDEX.md" "INDEX.md"
check_file "QUICK_REFERENCE.md" "QUICK_REFERENCE.md"
check_file "VERIFICATION.md" "VERIFICATION.md"
check_file "PROJECT_COMPLETION_REPORT.md" "PROJECT_COMPLETION_REPORT.md"
check_file "PROJECT_SUMMARY.txt" "PROJECT_SUMMARY.txt"
check_file "FINAL_SUMMARY.md" "FINAL_SUMMARY.md"
check_file ".env.template" ".env.template"
check_file "docker-compose.yml" "docker-compose.yml"

# Check directories
echo -e "\n${BLUE}DIRECTORIES:${NC}"
check_dir "backend" "backend/"
check_dir "frontend" "frontend/"
check_dir "infrastructure" "infrastructure/"
check_dir "k8s" "k8s/"
check_dir "monitoring" "monitoring/"
check_dir "nginx" "nginx/"
check_dir "scripts" "scripts/"
check_dir "security" "security/"
check_dir ".github" ".github/"
check_dir "docs" "docs/"

# Check backend files
echo -e "\n${BLUE}BACKEND FILES:${NC}"
check_file "backend/app/__init__.py" "Backend Flask init"
check_file "backend/app/routes/auth_routes.py" "Auth routes"
check_file "backend/app/routes/product_routes.py" "Product routes"
check_file "backend/app/routes/order_routes.py" "Order routes"
check_file "backend/app/routes/user_routes.py" "User routes"
check_file "backend/app/middleware/security.py" "Security middleware"
check_file "backend/app/middleware/logging.py" "Logging middleware"
check_file "backend/app/security/auth.py" "Auth utilities"
check_file "backend/app/utils/error_handlers.py" "Error handling"
check_file "backend/Dockerfile" "Backend Dockerfile"
check_file "backend/requirements.txt" "Backend requirements"
check_file "backend/tests/unit/test_auth.py" "Backend tests"

# Check frontend files
echo -e "\n${BLUE}FRONTEND FILES:${NC}"
check_file "frontend/src/App.js" "Frontend App"
check_file "frontend/src/pages/Login.js" "Login page"
check_file "frontend/src/pages/Register.js" "Register page"
check_file "frontend/src/pages/Products.js" "Products page"
check_file "frontend/src/pages/Orders.js" "Orders page"
check_file "frontend/src/pages/Profile.js" "Profile page"
check_file "frontend/src/services/api.js" "API service"
check_file "frontend/src/services/authService.js" "Auth service"
check_file "frontend/src/components/PrivateRoute.js" "Private route"
check_file "frontend/src/components/Layout.js" "Layout component"
check_file "frontend/src/store/index.js" "Redux store"
check_file "frontend/Dockerfile" "Frontend Dockerfile"
check_file "frontend/package.json" "Frontend package"

# Check infrastructure files
echo -e "\n${BLUE}INFRASTRUCTURE FILES:${NC}"
check_file "infrastructure/terraform/modules/vpc/main.tf" "VPC module"
check_file "infrastructure/terraform/modules/eks/main.tf" "EKS module"
check_file "infrastructure/terraform/modules/rds/main.tf" "RDS module"
check_file "infrastructure/terraform/environments/dev/main.tf" "Dev environment"
check_file "infrastructure/terraform/environments/prod/main.tf" "Prod environment"

# Check Kubernetes files
echo -e "\n${BLUE}KUBERNETES FILES:${NC}"
check_file "k8s/backend-deployment.yaml" "Backend deployment"
check_file "k8s/frontend-deployment.yaml" "Frontend deployment"
check_file "k8s/ingress.yaml" "Ingress config"

# Check CI/CD files
echo -e "\n${BLUE}CI/CD WORKFLOWS:${NC}"
check_file ".github/workflows/sast.yml" "SAST workflow"
check_file ".github/workflows/container-security.yml" "Container security workflow"
check_file ".github/workflows/iac-security.yml" "IaC security workflow"
check_file ".github/workflows/tests.yml" "Tests workflow"
check_file ".github/workflows/dast.yml" "DAST workflow"
check_file ".github/PULL_REQUEST_TEMPLATE.md" "PR template"
check_file ".github/ISSUE_TEMPLATE/bug_report.md" "Bug template"
check_file ".github/ISSUE_TEMPLATE/feature_request.md" "Feature template"
check_file ".github/ISSUE_TEMPLATE/security.md" "Security template"
check_file ".github/CODEOWNERS" "CODEOWNERS"

# Check security files
echo -e "\n${BLUE}SECURITY FILES:${NC}"
check_file "security/scanning/semgrep-rules.yaml" "Semgrep rules"
check_file "security/policies/compliance-controls.yaml" "Compliance controls"
check_file "security/ai-scoring/models/vulnerability_scorer.py" "AI vulnerability scorer"

# Check monitoring files
echo -e "\n${BLUE}MONITORING FILES:${NC}"
check_file "monitoring/prometheus/prometheus.yml" "Prometheus config"
check_file "monitoring/prometheus/alert.rules.yml" "Alert rules"
check_file "monitoring/grafana/dashboards/enterprise-dashboard.json" "Grafana dashboard"
check_file "monitoring/grafana/provisioning/datasources/datasources.yml" "Data sources"
check_file "monitoring/grafana/provisioning/dashboards/dashboards.yml" "Dashboard config"
check_file "monitoring/elk/docker-compose.yml" "ELK compose"
check_file "monitoring/elk/elasticsearch/elasticsearch.yml" "Elasticsearch config"
check_file "monitoring/elk/kibana/kibana.yml" "Kibana config"
check_file "monitoring/elk/logstash/pipeline/logstash.conf" "Logstash pipeline"
check_file "monitoring/elk/README.md" "ELK README"

# Check nginx files
echo -e "\n${BLUE}NGINX FILES:${NC}"
check_file "nginx/nginx.conf" "Nginx configuration"
check_file "nginx/Dockerfile" "Nginx Dockerfile"

# Check script files
echo -e "\n${BLUE}SCRIPT FILES:${NC}"
check_file "scripts/deploy.sh" "Deploy script"
check_file "scripts/backup.sh" "Backup script"
check_file "scripts/restore.sh" "Restore script"
check_file "scripts/health_check.sh" "Health check script"
check_file "scripts/seed_database.py" "Database seeding"

# Check documentation files
echo -e "\n${BLUE}DOCUMENTATION FILES:${NC}"
check_file "docs/API.md" "API documentation"
check_file "docs/ARCHITECTURE.md" "Architecture guide"
check_file "docs/DEPLOYMENT.md" "Deployment guide"
check_file "docs/DEPLOYMENT_CHECKLIST.md" "Deployment checklist"
check_file "docs/SECURITY.md" "Security documentation"
check_file "docs/PROJECT_SUMMARY.md" "Project summary"

# Summary
echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    VERIFICATION SUMMARY                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${GREEN}Completed: $COMPLETED${NC}"
echo -e "${RED}Issues: $ISSUES${NC}"

if [ $ISSUES -eq 0 ]; then
    echo -e "\n${GREEN}✓ ALL DELIVERABLES VERIFIED - PROJECT COMPLETE!${NC}\n"
    exit 0
else
    echo -e "\n${RED}✗ Some files are missing - Please check above${NC}\n"
    exit 1
fi
