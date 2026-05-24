# Contributing Guidelines

## 🤝 How to Contribute

We welcome contributions from all developers! Please follow these guidelines to ensure smooth collaboration.

## 📋 Code of Conduct

- Treat everyone with respect
- No harassment or discrimination
- Constructive feedback only
- Assume good intentions

## 🔄 Development Workflow

### 1. Fork & Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/ecommerce-devsecops.git
cd ecommerce-devsecops

# Add upstream
git remote add upstream https://github.com/yourorg/ecommerce-devsecops.git
```

### 2. Create Feature Branch

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feat/my-awesome-feature
```

**Branch naming convention:**
- `feat/feature-name` - New feature
- `fix/bug-name` - Bug fix
- `sec/security-fix` - Security patch
- `refactor/refactoring-name` - Code refactoring
- `docs/documentation-update` - Documentation
- `test/test-addition` - Tests

### 3. Make Changes

- Keep commits small and focused
- Write clear commit messages
- Add tests for new features
- Update documentation

### 4. Commit Messages

Follow semantic commit format:

```
type(scope): subject

body

footer
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `sec:` Security improvement
- `refactor:` Code restructuring
- `perf:` Performance improvement
- `docs:` Documentation
- `test:` Test updates
- `chore:` Maintenance

**Examples:**
```
feat(auth): implement JWT token refresh mechanism

fix(products): prevent SQL injection in filter query

sec(api): add rate limiting to authentication endpoints

docs(readme): update deployment instructions
```

### 5. Push Changes

```bash
git push origin feat/my-awesome-feature
```

### 6. Create Pull Request

- Open PR on GitHub
- Use PR template
- Link related issues
- Request reviewers
- Ensure CI/CD passes

## 🧪 Testing Requirements

### Backend Tests

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest tests/unit -v --cov=app

# Run integration tests
pytest tests/integration -v

# Check code style
flake8 app --max-line-length=120
black app --check
```

### Frontend Tests

```bash
cd frontend

# Install dependencies
npm ci

# Run tests
npm test

# Check code style
npm run lint

# Build check
npm run build
```

### Security Tests

```bash
# Run Semgrep
semgrep --config=security/scanning/semgrep-rules.yaml .

# Check for secrets
gitleaks detect --source local --verbose

# Dependency check
npm audit
pip audit
```

## 🔍 Code Review Process

### What Reviewers Look For

- ✅ Code quality and style
- ✅ Security implications
- ✅ Test coverage
- ✅ Documentation updates
- ✅ Performance impact
- ✅ Breaking changes
- ✅ Error handling
- ✅ Database considerations

### Review Checklist

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] New tests added
- [ ] No security issues
- [ ] Documentation updated
- [ ] No hardcoded values
- [ ] No sensitive data logged
- [ ] Backward compatible

## 🐛 Reporting Bugs

### Creating a Bug Report

1. Check if issue already exists
2. Use bug report template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots/logs
   - Environment details

### Bug Report Template

```markdown
## Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to...
2. Click on...
3. See error...

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g., macOS]
- Browser: [e.g., Chrome]
- Version: [e.g., 1.0.0]

## Logs
Relevant error logs or stack traces.
```

## 💡 Feature Requests

Include:
- Clear use case
- Proposed solution
- Alternative solutions
- Additional context

## 📚 Documentation Contribution

- Update README.md for major changes
- Add docstrings to new functions
- Update API documentation
- Add examples where helpful
- Fix typos and clarity issues

## 🔐 Security Vulnerability Reporting

**DO NOT** create public issues for security vulnerabilities.

Instead:
1. Email: security@company.com
2. Include details about vulnerability
3. Provide reproduction steps
4. Allow 90 days for patch before disclosure

## 📦 Local Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
export FLASK_ENV=development
flask run

# Server runs on http://localhost:5000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# App runs on http://localhost:3000
```

### Docker Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🎯 Pull Request Checklist

Before submitting:

- [ ] Branch is updated with main
- [ ] Commits are logical and well-messaged
- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or noted)
- [ ] Security issues addressed
- [ ] Performance impact minimal
- [ ] Ready for review

## 📊 Contribution Recognition

Contributors are recognized through:
- GitHub contributors page
- CONTRIBUTORS.md file
- Release notes
- Community highlights

## 🚫 What We Won't Accept

- PRs without tests
- Code with security issues
- Documentation-only issues without changes
- Duplicate issues
- Commercial solicitation
- Spam or off-topic content

## 📞 Getting Help

- **Questions:** Discuss section
- **Bug reports:** Issues tracker
- **Security:** security@company.com
- **General:** team@company.com

## 🏆 Contributors

Thank you to all our contributors!

---

**Happy contributing! Let's build something great together. 🚀**
