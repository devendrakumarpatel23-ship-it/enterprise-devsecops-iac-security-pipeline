# Security Guidelines

## 🔒 Security Principles

### Zero Trust Architecture
- Never trust, always verify
- Least privilege access
- Defense in depth
- Secure by default

## 🛡️ Authentication & Authorization

### JWT Implementation
- **Expiration:** Access tokens (1 hour), Refresh tokens (30 days)
- **Claims:** user_id, email, roles, iat, exp
- **Storage:** HttpOnly cookies (frontend)
- **Validation:** Always verify signature

### Password Policy
- Minimum 12 characters
- Must include uppercase, lowercase, digit, special char
- Bcrypt hashing with 12 rounds
- No password reuse (last 5 passwords)
- Change every 90 days

### RBAC (Role-Based Access Control)
- `admin` - Full system access
- `moderator` - Content management
- `user` - Standard user access
- `guest` - Limited read-only access

## 🔐 Data Protection

### Encryption in Transit
- TLS 1.3 mandatory
- HSTS headers
- Certificate pinning (mobile apps)

### Encryption at Rest
- MongoDB: AES-256 encryption
- Database: AWS KMS managed keys
- Backups: Encrypted copies

### PII Protection
- Field-level encryption for sensitive data
- Tokenization for payment data
- Data minimization principles
- Retention policies

## 🛑 Input Validation

### Validation Rules
```python
# Email
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

# Phone
^\+?1?\d{9,15}$

# URLs
^https://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$

# Strong Password
^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{12,}$
```

### Sanitization
- HTML entities encoding
- SQL parameter binding
- Command injection prevention
- Path traversal prevention

## 🚫 Common Vulnerabilities Prevention

### SQL Injection
- ✅ Parameterized queries
- ✅ ORM usage (PyMongo)
- ✅ Input validation
- ✅ Principle of least privilege

### XSS Prevention
- ✅ Output encoding
- ✅ Content Security Policy
- ✅ Sanitize user input
- ✅ HttpOnly cookies

### CSRF Prevention
- ✅ CSRF tokens
- ✅ SameSite cookie attribute
- ✅ Origin validation
- ✅ Referer checking

### Authentication Bypass
- ✅ Secure token generation
- ✅ Token expiration
- ✅ Secure storage
- ✅ Protected endpoints

### Insecure Deserialization
- ✅ No pickle usage
- ✅ JSON validation
- ✅ Type checking
- ✅ Whitelist allowed types

## 🔍 Security Testing

### SAST (Static Analysis)
- Semgrep for code patterns
- SonarQube for code quality
- ESLint for JavaScript
- Bandit for Python

### SCA (Dependency Scanning)
- npm audit
- pip audit
- Snyk scanning
- License compliance

### DAST (Dynamic Testing)
- OWASP ZAP for web apps
- API security testing
- Penetration testing
- Load testing under attack

### IaC Security
- Checkov for Terraform
- TFLint for linting
- Policy as Code
- Compliance validation

## 📋 Secure Coding Practices

### DO's
- ✅ Use strong cryptography
- ✅ Validate all inputs
- ✅ Use parameterized queries
- ✅ Implement proper logging
- ✅ Handle errors securely
- ✅ Use security headers
- ✅ Keep dependencies updated
- ✅ Review code changes
- ✅ Use environment variables for secrets
- ✅ Implement rate limiting

### DON'Ts
- ❌ Hardcode secrets
- ❌ Use weak algorithms
- ❌ Log sensitive data
- ❌ Trust user input
- ❌ Use eval/exec
- ❌ Store passwords in plaintext
- ❌ Use public repositories for private code
- ❌ Disable security features
- ❌ Share credentials
- ❌ Use deprecated libraries

## 🔑 Secrets Management

### GitHub Secrets
```bash
# Store these as repository secrets
SONAR_TOKEN
SONAR_HOST_URL
SNYK_TOKEN
GITLEAKS_LICENSE
REGISTRY_USERNAME
REGISTRY_PASSWORD
DB_PASSWORD
JWT_SECRET_KEY
```

### Environment Variables
```bash
# .env (NEVER commit this file)
MONGODB_URI
REDIS_URI
JWT_SECRET_KEY
ENCRYPTION_KEY
ALLOWED_ORIGINS
```

### Secret Rotation
- Automatic rotation every 90 days
- No service disruption
- Audit logging
- Emergency rotation process

## 🚨 Incident Response

### Severity Levels
- **CRITICAL** - Immediate response required
- **HIGH** - Response within 1 hour
- **MEDIUM** - Response within 24 hours
- **LOW** - Response within 1 week

### Response Steps
1. Identify and confirm vulnerability
2. Assess impact and scope
3. Contain the threat
4. Eradicate the vulnerability
5. Recover systems
6. Post-incident review

### Reporting
- Email: security@company.com
- Do NOT create public issues
- PGP key available for encrypted reports
- Response within 24 hours

## 📚 Compliance

### PCI-DSS (Payment Card Industry)
- Secure network architecture
- Protect cardholder data
- Vulnerability management
- Access control measures
- Regularly monitor and test
- Information security policy

### OWASP Top 10
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Authentication Failures
- A08: Data Integrity Failures
- A09: Logging & Monitoring
- A10: SSRF

### CIS Benchmarks
- Asset inventory
- Software inventory
- Data protection
- Secure configuration
- Access control
- Incident response

## 🔄 Security Update Process

1. Monitor security advisories
2. Assess impact on project
3. Test updates in dev environment
4. Merge to main branch
5. Deploy to staging
6. Monitor for issues
7. Deploy to production
8. Document changes

---

**Report security issues responsibly. See [SECURITY.md](../SECURITY.md)**
