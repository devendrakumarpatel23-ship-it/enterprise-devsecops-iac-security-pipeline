# Quick Reference Guide

## 🚀 Start Here

**For new users:** Read in this order:
1. [README.md](README.md) - Overview and quick start (5 min)
2. [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design (10 min)
3. [API.md](docs/API.md) - API reference (10 min)
4. Then explore specific components

---

## 📋 Common Commands

### 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Remove everything
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Scale services
docker-compose up -d --scale backend=3
```

### 🧪 Testing Commands

**Backend:**
```bash
cd backend
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app

# Run specific test
pytest tests/unit/test_auth.py -v
```

**Frontend:**
```bash
cd frontend
npm install

# Run tests
npm test

# With coverage
npm test -- --coverage

# Run linter
npm run lint

# Fix linter issues
npm run lint:fix
```

### 🔒 Security Scanning

```bash
# SAST with Semgrep
semgrep --config=security/scanning/semgrep-rules.yaml .

# Secrets detection
gitleaks detect --source local

# Container scan
trivy image backend:latest

# Infrastructure scan
checkov -d infrastructure/terraform

# Dependency audit
npm audit
pip audit
```

### ☸️ Kubernetes Commands

```bash
# Get resources
kubectl get pods -n ecommerce
kubectl get services -n ecommerce
kubectl get deployments -n ecommerce

# View logs
kubectl logs -f deployment/backend -n ecommerce

# Port forward
kubectl port-forward svc/backend 5000:5000 -n ecommerce

# Scale deployment
kubectl scale deployment backend --replicas=3 -n ecommerce

# Describe resource
kubectl describe pod <pod-name> -n ecommerce

# Delete resource
kubectl delete deployment backend -n ecommerce
```

### 🏗️ Terraform Commands

```bash
cd infrastructure/terraform/environments/dev

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply

# Destroy
terraform destroy

# Format check
terraform fmt -check

# Validate
terraform validate
```

---

## 🔐 Authentication Workflow

### 1. Register
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

### 2. Login (Get Token)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Use Token
```bash
curl -X GET http://localhost:5000/api/products \
  -H "Authorization: Bearer <TOKEN_FROM_LOGIN>"
```

### 4. Refresh Token
```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer <REFRESH_TOKEN>"
```

---

## 🌐 Service URLs

### Local Development

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | - |
| Backend API | http://localhost:5000 | - |
| MongoDB | mongodb://localhost:27017 | admin/admin123 |
| Redis | redis://localhost:6379 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3001 | admin/admin |
| SonarQube | http://localhost:9000 | admin/admin |

### Production (AWS)

| Service | URL |
|---------|-----|
| Frontend | https://www.ecommerce.example.com |
| API | https://api.ecommerce.example.com |
| RDS Database | ecommerce-db.xxxxxx.us-east-1.rds.amazonaws.com |

---

## 📊 Monitoring & Alerts

### Prometheus
- **URL:** http://localhost:9090
- **Queries:** Check `/graph` tab
- **Alerts:** Check `/alerts` tab

### Grafana
- **URL:** http://localhost:3001
- **User:** admin / admin
- **Dashboard:** Home > Dashboards

### Alert Rules
View in: `monitoring/prometheus/alert.rules.yml`

Common alerts:
- API down
- High error rate
- Database connection issues
- Memory/CPU usage high

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check Docker daemon
docker --version

# Check port conflicts
lsof -i :5000

# Remove containers
docker-compose rm -f

# Rebuild
docker-compose build --no-cache
```

### Database Connection Failed

```bash
# Check MongoDB
docker exec ecommerce-devsecops-mongo mongosh

# Check Redis
docker exec ecommerce-devsecops-redis redis-cli ping

# Reset database
docker-compose down -v
docker-compose up -d
```

### API Not Responding

```bash
# Check container logs
docker-compose logs backend

# Check health endpoint
curl http://localhost:5000/health

# Rebuild image
docker-compose build --no-cache backend
```

### Tests Failing

```bash
# Check test output
pytest tests/ -v -s

# Check requirements
pip install -r requirements.txt --upgrade

# Clear cache
rm -rf .pytest_cache __pycache__
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app/__init__.py` | Flask app initialization |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node dependencies |
| `docker-compose.yml` | Local dev environment |
| `.github/workflows/` | CI/CD pipelines |
| `infrastructure/terraform/` | Cloud infrastructure |
| `monitoring/prometheus/` | Metrics & alerts |
| `security/scanning/` | Security rules |
| `docs/` | Documentation |

---

## 🔑 Environment Variables

### Backend (.env)
```
FLASK_ENV=development
FLASK_APP=app
JWT_SECRET_KEY=your-secret-key
MONGODB_URI=mongodb://admin:admin123@localhost:27017/ecommerce
REDIS_URI=redis://localhost:6379
LOG_LEVEL=INFO
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

---

## 📚 Documentation Map

```
docs/
├── README.md - Project overview
├── ARCHITECTURE.md - System design
├── API.md - API reference
├── DEPLOYMENT.md - Deployment guide
├── SECURITY.md - Security policies
├── CONTRIBUTING.md - Development guide
├── PROJECT_SUMMARY.md - Project overview
└── DEPLOYMENT_CHECKLIST.md - Verification
```

---

## 🚀 Deployment Workflow

### Development
```bash
# Run locally
docker-compose up -d

# Test
pytest && npm test

# Commit & push
git push origin feature-branch
```

### Staging
```bash
# GitHub Actions auto-runs on PR

# Review results in Actions tab

# Merge to main branch
```

### Production
```bash
# Run deployment script
./scripts/deploy.sh prod

# Verify
kubectl get pods -n ecommerce

# Monitor
Check Grafana dashboards
```

---

## 🔍 Security Checklist

Before deploying:
- [ ] All tests passing
- [ ] No SAST issues
- [ ] No secrets exposed
- [ ] Containers scanned
- [ ] Terraform validated
- [ ] Monitoring configured
- [ ] Backups enabled
- [ ] Secrets secured

---

## 📞 Help & Support

**Documentation:** See [docs/](docs/) folder

**Issues:** GitHub Issues tracker

**Security:** [SECURITY.md](SECURITY.md)

**Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💡 Pro Tips

1. **Development:** Use `docker-compose up -d` for local environment
2. **Testing:** Run tests before pushing: `pytest && npm test`
3. **Security:** Check logs regularly: `docker-compose logs -f`
4. **Monitoring:** Watch Grafana for anomalies
5. **Scaling:** Use Kubernetes in production
6. **Backups:** Ensure backups run daily
7. **Documentation:** Keep it up-to-date

---

## 🎯 Common Workflows

### Add New API Endpoint

1. Create route in `backend/app/routes/`
2. Add tests in `backend/tests/`
3. Update `docs/API.md`
4. Push to GitHub
5. Wait for CI/CD to pass

### Deploy to Production

1. Test locally: `docker-compose up -d`
2. Run security scan: `semgrep --config=security/scanning/semgrep-rules.yaml .`
3. Push to main branch
4. Review GitHub Actions results
5. Run: `./scripts/deploy.sh prod`
6. Monitor: Check Grafana

### Report Security Issue

1. **DO NOT** create public issue
2. Email: security@company.com
3. Include vulnerability details
4. Provide reproduction steps
5. Allow 90 days for patch

---

**Last Updated:** May 2024  
**Quick Reference Version:** 1.0  
**Status:** Current
