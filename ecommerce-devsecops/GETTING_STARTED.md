# 🚀 GETTING STARTED - 5 MINUTE SETUP

## Quick Start for Development

### 1️⃣ Prerequisites (Install if needed)
- Docker & Docker Compose
- Git
- Node.js 18+ (optional, for local frontend dev)
- Python 3.11+ (optional, for local backend dev)

### 2️⃣ Clone & Setup (1 minute)
```bash
cd ecommerce-devsecops
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 3️⃣ Start Services (2 minutes)
```bash
# Start all 13 services
docker-compose up -d

# Wait for services to be ready (~2 min)
sleep 120

# Check status
docker-compose ps
```

### 4️⃣ Access Applications (1 minute)

**Frontend (React App)**
```
URL: http://localhost:3000
Default Credentials:
  Email: user@example.com
  Password: Password123!
```

**Backend API**
```
URL: http://localhost:5000
Health Check: http://localhost:5000/health
```

**Admin Dashboards**
```
SonarQube:   http://localhost:9000 (admin/admin)
Grafana:     http://localhost:3001 (admin/admin)
Prometheus:  http://localhost:9090
Kibana:      http://localhost:5601
```

### 5️⃣ Verify Everything Works (1 minute)
```bash
# Backend health check
curl http://localhost:5000/health

# Frontend loads
curl http://localhost:3000

# Services running
docker-compose ps
```

✅ **You're ready!** The full stack is running locally.

---

## 🧪 Quick Testing

### Run Backend Tests
```bash
docker exec ecommerce-backend pytest tests/ -v --cov
```

### Run Frontend Tests
```bash
docker exec ecommerce-frontend npm test
```

### Test API Endpoints
```bash
# Register new user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","username":"testuser"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Get products (no auth needed)
curl http://localhost:5000/products
```

---

## 📚 Quick Reference Commands

### Docker
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Rebuild services
docker-compose up -d --build
```

### Backend
```bash
# Access backend shell
docker exec -it ecommerce-backend bash

# Run tests
docker exec ecommerce-backend pytest

# See logs
docker logs ecommerce-backend -f
```

### Frontend
```bash
# Access frontend shell
docker exec -it ecommerce-frontend bash

# Run tests
docker exec ecommerce-frontend npm test

# See logs
docker logs ecommerce-frontend -f
```

### Database
```bash
# Access MongoDB
docker exec -it mongo mongosh

# View MongoDB data
docker exec mongo mongosh --eval "db.users.find()"
```

---

## 🔍 Key Features to Test

1. **Authentication** (5 min)
   - Register new user
   - Login with credentials
   - Try without auth (should fail)

2. **Product Management** (5 min)
   - View products list
   - Search products
   - Filter by category

3. **Orders** (5 min)
   - Create new order
   - View order details
   - Track order status

4. **User Profile** (5 min)
   - Update profile info
   - Change password
   - View account settings

5. **Security** (10 min)
   - Test XSS protection
   - Test CSRF token
   - Test rate limiting

---

## 📊 Monitoring & Observability

### View Metrics (Prometheus)
1. Open http://localhost:9090
2. Query metrics:
   - `api_requests_total`
   - `api_request_duration_seconds`
   - `database_query_duration_seconds`

### View Dashboards (Grafana)
1. Open http://localhost:3001
2. Login: admin/admin
3. Browse pre-built dashboards
4. Create custom dashboards

### View Logs (Kibana)
1. Open http://localhost:5601
2. Explore logs from past 24 hours
3. Search for errors

### Check Health
```bash
# Backend
curl http://localhost:5000/health

# All services
docker-compose ps
```

---

## 🐛 Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Clean up and restart
docker-compose down
docker-compose up -d --build
```

### Port already in use
```bash
# Find process on port
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database connection failed
```bash
# Check MongoDB logs
docker logs mongo

# Verify connection string in .env
cat backend/.env | grep MONGO
```

### Tests failing
```bash
# Run with verbose output
docker exec ecommerce-backend pytest -vv

# Run specific test
docker exec ecommerce-backend pytest tests/unit/test_auth.py -v
```

---

## 📖 Next Steps

1. **Read Documentation**
   ```
   Start with: README.md
   Then read: QUICK_REFERENCE.md
   Deep dive: docs/ARCHITECTURE.md
   ```

2. **Explore Code**
   ```
   Backend: backend/app/routes/
   Frontend: frontend/src/pages/
   Tests: backend/tests/
   ```

3. **Deploy to AWS** (30 minutes)
   ```
   See: docs/DEPLOYMENT.md
   ```

4. **Run Security Scans**
   ```
   See: .github/workflows/
   ```

---

## 🎯 Learning Path

**For Beginners (2 hours)**
- [ ] Read README.md
- [ ] Run docker-compose up
- [ ] Test the application
- [ ] Explore Grafana dashboard

**For Intermediate (4 hours)**
- [ ] Review API documentation (docs/API.md)
- [ ] Study architecture (docs/ARCHITECTURE.md)
- [ ] Read backend code
- [ ] Read frontend code

**For Advanced (8+ hours)**
- [ ] Study Terraform modules
- [ ] Review security implementation
- [ ] Analyze CI/CD workflows
- [ ] Plan AWS deployment

**For DevSecOps (12+ hours)**
- [ ] Deploy to AWS
- [ ] Configure monitoring
- [ ] Test security scanning
- [ ] Practice incident response

---

## ✅ Validation Checklist

- [ ] Docker & Docker Compose installed
- [ ] Services starting successfully
- [ ] Frontend accessible at localhost:3000
- [ ] Backend responding at localhost:5000
- [ ] Can register new user
- [ ] Can login successfully
- [ ] Can view products
- [ ] Can create order
- [ ] Grafana dashboard visible
- [ ] Tests passing

---

## 💡 Pro Tips

1. **Watch logs in real-time**
   ```bash
   docker-compose logs -f backend frontend
   ```

2. **Connect to MongoDB directly**
   ```bash
   docker exec -it mongo mongosh
   > use ecommerce
   > db.users.find()
   ```

3. **Run specific test**
   ```bash
   docker exec ecommerce-backend pytest tests/unit/test_auth.py::test_register_success -v
   ```

4. **View environment variables**
   ```bash
   docker exec ecommerce-backend env | grep -i mongo
   ```

5. **Check performance metrics**
   ```bash
   curl http://localhost:9090/api/v1/query?query=api_request_duration_seconds
   ```

---

## 🆘 Need Help?

1. **Check logs first**
   ```bash
   docker-compose logs backend
   ```

2. **Verify environment variables**
   ```bash
   cat backend/.env
   cat frontend/.env
   ```

3. **Restart services**
   ```bash
   docker-compose restart
   ```

4. **Check documentation**
   - QUICK_REFERENCE.md - Quick commands
   - docs/DEPLOYMENT_CHECKLIST.md - Verification
   - docs/DEPLOYMENT.md - Troubleshooting

---

## 🎉 You're All Set!

The enterprise DevSecOps e-commerce platform is running!

**Next: Explore the application and continue learning!**

For detailed guides, see:
- [Complete Documentation](docs/)
- [API Reference](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Quick Reference](QUICK_REFERENCE.md)

Happy coding! 🚀

---

*For production deployment, see docs/DEPLOYMENT.md*
*For security details, see SECURITY.md*
*For contribution guidelines, see CONTRIBUTING.md*
