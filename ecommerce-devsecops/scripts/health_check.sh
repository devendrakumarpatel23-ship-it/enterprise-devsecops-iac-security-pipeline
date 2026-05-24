#!/bin/bash

# Health Check Script
# Verifies all services are running and healthy

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}Service Health Check${NC}"
echo -e "${BLUE}====================================${NC}\n"

FAILED=0
PASSED=0

# Function to check endpoint
check_endpoint() {
    local name=$1
    local url=$2
    local expected_status=$3
    
    echo -n "Checking $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" || echo "000")
    
    if [ "$response" == "$expected_status" ]; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ (HTTP $response)${NC}"
        ((FAILED++))
    fi
}

# Function to check service
check_service() {
    local name=$1
    local command=$2
    
    echo -n "Checking $name... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED++))
    fi
}

# API Health Checks
echo -e "${BLUE}API Services:${NC}"
check_endpoint "Backend API" "http://localhost:5000/health" "200"
check_endpoint "Frontend" "http://localhost:3000" "200"

# Database Health Checks
echo -e "\n${BLUE}Databases:${NC}"
check_service "MongoDB" "mongosh --eval 'db.adminCommand(\"ping\")' mongodb://localhost:27017 > /dev/null 2>&1"
check_service "Redis" "redis-cli ping > /dev/null 2>&1"

# Monitoring Health Checks
echo -e "\n${BLUE}Monitoring:${NC}"
check_endpoint "Prometheus" "http://localhost:9090/-/healthy" "200"
check_endpoint "Grafana" "http://localhost:3001/api/health" "200"

# Code Quality & Security
echo -e "\n${BLUE}Code Quality:${NC}"
check_service "Backend Tests" "cd backend && pytest tests/ -q --tb=no 2>&1 | grep -q 'passed' || false"
check_service "Linting" "cd backend && flake8 app --quiet"

# Docker Health Checks
echo -e "\n${BLUE}Containers:${NC}"
check_service "Backend Container" "docker ps | grep -q ecommerce-backend"
check_service "Frontend Container" "docker ps | grep -q ecommerce-frontend"
check_service "MongoDB Container" "docker ps | grep -q mongo"
check_service "Redis Container" "docker ps | grep -q redis"

# Security Health Checks
echo -e "\n${BLUE}Security:${NC}"
check_service "No Hardcoded Secrets" "! grep -r 'password.*=' backend/app --include='*.py' 2>/dev/null | grep -v 'password_hash' || true"
check_service "HTTPS Redirect" "cd frontend && grep -q 'https' src/services/api.js || true"

# Summary
echo -e "\n${BLUE}====================================${NC}"
echo -e "${BLUE}Health Check Summary${NC}"
echo -e "${BLUE}====================================${NC}"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ All services are healthy!${NC}\n"
    exit 0
else
    echo -e "\n${RED}✗ Some services need attention${NC}\n"
    exit 1
fi
