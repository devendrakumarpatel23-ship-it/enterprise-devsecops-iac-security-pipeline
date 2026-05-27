# 🚀 Enterprise Security Platform - Getting Started Guide

## 📖 For Different User Roles

---

## 👨‍💼 For Security Leaders & CISOs

### What You Need to Know (5 minutes)

The Enterprise Security Platform provides:
- **Real-time Security Posture**: Security score from 0-100 with trend analysis
- **Risk Quantification**: Quantified organizational risk with impact analysis
- **Compliance Automation**: Automated multi-framework compliance validation
- **Executive Dashboards**: Business-focused security metrics and KPIs
- **Incident Timeline**: Complete incident investigation with forensics

### Quick Dashboard Tour

1. **Navigate to Grafana**: http://localhost:3000
2. **Look at "Security KPI Metrics"** (top row):
   - Security Score: Your overall posture (aim >85)
   - Critical Vulnerabilities: Count of critical CVEs
   - Open Incidents: Active security incidents
   - Compliance Score: Framework compliance percentage
3. **Review "Remediation Priority"**: 
   - Critical items need immediate attention (4 hours)
   - High items need action within 24 hours
4. **Check "Compliance" section**:
   - Framework-by-framework breakdown
   - Gap analysis and remediation tracking

### Key Metrics to Monitor

```
Daily Review:
- Security Score trend (should be stable/improving)
- New critical vulnerabilities (should be zero)
- Mean Time to Respond (should be <4 hours)

Weekly Review:
- Compliance score trend
- Remediation rate
- Attack attempts
- Policy violations

Monthly Review:
- Risk score trend
- Incident count
- Patch rate
- Framework compliance
```

### First 30 Days Action Plan

**Week 1:**
- Review executive dashboard daily
- Understand current security posture
- Identify top 3 risks

**Week 2:**
- Review compliance gaps
- Create remediation plan
- Assign owners to action items

**Week 3:**
- Monitor remediation progress
- Review incident response capability
- Test alert system

**Week 4:**
- Report results to board
- Plan quarterly review
- Set targets for next quarter

---

## 🔐 For Security Analysts & SOC Teams

### Platform Access & Setup

**Login to Dashboard:**
```
Grafana: http://localhost:3000
Username: admin
Password: SecurePassword123!
```

**Create Your First Alert:**
1. Go to Alerts tab
2. Click "New Alert"
3. Set threshold (e.g., CVE score > 7.0)
4. Configure notification (email, Slack)
5. Save and test

### Understanding Alert Severity

| Level | Color | Action | Response Time |
|-------|-------|--------|----------------|
| CRITICAL | 🔴 Red | Page on-call | < 15 min |
| HIGH | 🟠 Orange | Alert team | < 1 hour |
| MEDIUM | 🟡 Yellow | Create ticket | < 4 hours |
| LOW | 🟢 Green | Log & track | < 1 day |

### Daily SOC Tasks

```
Morning (09:00):
1. Review overnight alerts
2. Check threat events
3. Review compliance status
4. Check system health

During day:
5. Investigate high/critical alerts
6. Update incident timelines
7. Coordinate with teams
8. Document findings

End of day (17:00):
9. Summarize incidents
10. Update dashboards
11. Prepare handoff notes
12. Archive logs
```

### Common Alert Scenarios

**Scenario 1: Critical CVE Detected**
1. Alert received for CVE with CVSS 9.0+
2. Check "MITRE Matrix" for attack techniques
3. Review "Compliance Impact" section
4. Create incident ticket
5. Notify affected teams
6. Track remediation

**Scenario 2: Unauthorized Access Attempt**
1. Alert shows unauthorized API access
2. Check "Threat Timeline" for pattern
3. Investigate failed login attempts
4. Check IP reputation
5. Block if necessary
6. Document in timeline

**Scenario 3: Compliance Violation**
1. Alert for PCI-DSS control violation
2. Check "Compliance" dashboard
3. Review "Gap Analysis"
4. Create remediation ticket
5. Track progress
6. Verify fix

### Key Reports to Generate

**Daily Report:**
```bash
curl http://localhost:5000/api/security/overview
# Shows: Alerts, risk score, compliance status
```

**Weekly Report:**
```bash
curl http://localhost:5000/api/security/report/download?format=json&days=7
# Shows: Trends, resolved incidents, metrics
```

**Monthly Report:**
```bash
curl http://localhost:5000/api/security/report/download?format=json&days=30
# Shows: Complete analysis with recommendations
```

### Useful Keyboard Shortcuts

- `Ctrl+Shift+A` - Jump to Alerts
- `Ctrl+Shift+D` - Jump to Dashboard
- `Ctrl+Shift+R` - Refresh data
- `?` - Help menu

---

## 👨‍💻 For DevOps & Infrastructure Teams

### Platform Deployment

**Prerequisites:**
```bash
# Check system requirements
docker --version        # 20.10+
docker-compose --version # 1.29+
python3 --version       # 3.10+
```

**Deploy in 3 Steps:**

```bash
# Step 1: Start monitoring stack
cd monitoring
docker-compose up -d
cd ..

# Step 2: Verify all services running
docker-compose ps
# Expected: 9 services in "Up" state

# Step 3: Access dashboards
open http://localhost:3000  # Grafana
open http://localhost:9090  # Prometheus
open http://localhost:5601  # Kibana
```

### Configuration Management

**Edit Prometheus Scrape Targets:**
```yaml
# monitoring/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'backend-api'
    static_configs:
      - targets: ['localhost:5000']
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

**Add Custom Alert Rules:**
```yaml
# monitoring/prometheus/alert.rules.yml
- alert: MyCustomAlert
  expr: my_metric > 100
  for: 5m
  annotations:
    summary: "Custom alert triggered"
```

**Restart Services:**
```bash
docker-compose restart prometheus
docker-compose restart grafana
docker-compose logs -f grafana  # View logs
```

### Health Checks

**Monitor Service Health:**
```bash
# Prometheus
curl -s http://localhost:9090/-/healthy

# Grafana
curl -s http://localhost:3000/api/health

# Elasticsearch
curl -s http://localhost:9200/_cluster/health | jq

# Logstash
curl -s http://localhost:9600/_node/stats | jq
```

**Common Issues:**

| Issue | Solution |
|-------|----------|
| Service won't start | Check logs: `docker-compose logs <service>` |
| Port already in use | Change port in docker-compose.yml |
| Out of disk space | Prune old data: `docker system prune -a` |
| High memory usage | Increase docker-compose memory limits |
| Slow queries | Check Elasticsearch health & add indices |

### Kubernetes Deployment

**Deploy to Kubernetes:**
```bash
# Apply deployments
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

**Scale Services:**
```bash
# Scale backend
kubectl scale deployment backend --replicas=3

# Scale frontend
kubectl scale deployment frontend --replicas=3

# Check status
kubectl get pods -l app=backend
```

---

## 📊 For Data Analytics & Compliance Teams

### Generating Compliance Reports

**PCI-DSS Report:**
```bash
curl http://localhost:5000/api/security/compliance-status \
  --header "framework=PCI-DSS" \
  > pci-dss-report.json
```

**NIST CSF Report:**
```bash
curl http://localhost:5000/api/security/compliance-status \
  --header "framework=NIST" \
  > nist-csf-report.json
```

**All Frameworks Report:**
```bash
curl http://localhost:5000/api/security/report/download \
  --header "format=json" \
  > complete-compliance-report.json
```

### Key Metrics to Track

**Compliance Metrics:**
```
- PCI-DSS: Target 100%, Current ___%
- OWASP: Target 95%, Current ___%
- CIS: Target 90%, Current ___%
- NIST: Target 95%, Current ___%
- SOC2: Target 100%, Current ___%
- ISO 27001: Target 90%, Current ___%
```

**Remediation Metrics:**
```
- Critical items: __ open, __ resolved
- Control gaps: __ identified, __ remediated
- Policy violations: __ detected, __ fixed
- Audit readiness: __ days until audit
```

### Audit Preparation Checklist

**1 Month Before Audit:**
- [ ] Generate compliance baseline report
- [ ] Identify gaps
- [ ] Create remediation plan
- [ ] Assign owners

**2 Weeks Before Audit:**
- [ ] Verify remediation progress
- [ ] Prepare supporting documentation
- [ ] Train team on audit process
- [ ] Set up audit environment

**1 Week Before Audit:**
- [ ] Final compliance check
- [ ] Verify all controls
- [ ] Prepare evidence files
- [ ] Brief auditors on findings

**After Audit:**
- [ ] Document audit findings
- [ ] Create action plan
- [ ] Track remediation
- [ ] Schedule follow-up audit

---

## 🎯 For Development Teams

### Integrating Security into CI/CD

**GitHub Actions Integration:**
```yaml
# .github/workflows/advanced-security-gates.yml
- name: Run security scan
  run: |
    semgrep --config=p/security-audit .
    dependencycheck --scan . --format JSON
    trivy image myapp:latest
```

**Blocking on Findings:**
```bash
# Automatic block if critical vulnerabilities found
if [ $CRITICAL_COUNT -gt 0 ]; then
  echo "Critical vulnerabilities found. Blocking deployment."
  exit 1
fi
```

### Security Scanning Commands

**SAST Scanning (Find code vulnerabilities):**
```bash
semgrep --config=p/owasp-top-ten .
semgrep --config=p/cwe-top-25 .
```

**Dependency Scanning (Find vulnerable libraries):**
```bash
pip-audit
npm audit
```

**Container Scanning (Find image vulnerabilities):**
```bash
trivy image myapp:latest
trivy image myapp:latest --severity HIGH,CRITICAL
```

**SBOM Generation (Bill of Materials):**
```bash
cyclonedx-bom -o sbom.xml
cyclonedx-bom -o sbom.json --format json
```

### Pre-Commit Hooks

**Setup local scanning:**
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: local
    hooks:
      - id: semgrep
        name: Semgrep scan
        entry: semgrep --config=p/security-audit
        language: system
        stages: [commit]
      - id: bandit
        name: Python security check
        entry: bandit
        language: system
        types: [python]
EOF

# Install hooks
pre-commit install
```

---

## 🎓 For New Team Members

### First Day Orientation (1 hour)

**1. Understand the Platform (15 min)**
- What: Enterprise security monitoring platform
- Why: Unified threat visibility and compliance
- How: Cloud-native, containerized, microservices

**2. Access Dashboards (15 min)**
```bash
# Bookmark these
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Kibana: http://localhost:5601
- API: http://localhost:5000/api/security
```

**3. Review Documentation (15 min)**
- Read: IMPLEMENTATION_SUMMARY.md
- Skim: QUICK_REFERENCE_SECURITY.md
- Bookmark: ARCHITECTURE_OVERVIEW.md

**4. Ask Questions (15 min)**
- Schedule time with team lead
- Join Slack channel: #security-platform
- Review FAQ wiki

### First Week Tasks

- [ ] Set up local environment
- [ ] Deploy monitoring stack locally
- [ ] Access all dashboards
- [ ] Run sample reports
- [ ] Create test alert
- [ ] Investigate sample incident
- [ ] Read complete documentation
- [ ] Schedule 1:1 with mentor

### First Month Goals

- [ ] Can navigate dashboards independently
- [ ] Understand alert flow and investigation
- [ ] Can generate basic reports
- [ ] Familiar with API endpoints
- [ ] Know how to add custom alerts
- [ ] Understand compliance framework
- [ ] Can respond to common issues
- [ ] Contributed to team runbook

---

## 🆘 Troubleshooting Common Issues

### Issue: Dashboard Won't Load

**Symptom**: Grafana page shows error

**Solution**:
```bash
# Check Grafana status
docker-compose ps grafana

# View logs
docker-compose logs grafana

# Restart if needed
docker-compose restart grafana

# Verify connectivity
curl http://localhost:3000
```

### Issue: No Data in Prometheus

**Symptom**: Prometheus shows "no data"

**Solution**:
```bash
# Check scrape targets
curl http://localhost:9090/api/v1/targets

# View alert rules
curl http://localhost:9090/api/v1/rules

# Verify backend is running
curl http://localhost:5000/api/security/overview
```

### Issue: Elasticsearch Errors

**Symptom**: "Connection refused" errors

**Solution**:
```bash
# Check Elasticsearch status
curl http://localhost:9200/_cluster/health

# View logs
docker-compose logs elasticsearch

# Check disk space
df -h

# Increase memory if needed
# Edit docker-compose.yml: environment: ES_JAVA_OPTS="-Xms2g -Xmx2g"
```

### Issue: Alert Not Triggering

**Symptom**: Alert configured but not firing

**Solution**:
```bash
# Test alert rule
curl http://localhost:9090/api/v1/query?query=<your-metric>

# Check AlertManager
curl http://localhost:9093/api/v1/alerts

# Verify notification config
# Edit monitoring/prometheus/alert.rules.yml
# Restart Prometheus: docker-compose restart prometheus
```

---

## 📞 Getting Help

### Documentation
- **Main README**: README.md
- **Getting Started**: GETTING_STARTED.md
- **API Reference**: docs/API.md
- **Deployment**: docs/DEPLOYMENT.md
- **Architecture**: ARCHITECTURE_OVERVIEW.md

### Support Channels
- **Email**: security-platform@enterprise.com
- **Slack**: #security-platform
- **Wiki**: https://wiki.enterprise.com/security
- **GitHub Issues**: Report bugs and request features

### Office Hours
- **Monday**: 10:00 AM - 11:00 AM
- **Wednesday**: 3:00 PM - 4:00 PM
- **Friday**: 9:00 AM - 10:00 AM

---

## ✅ Checklist for Getting Started

- [ ] Deployed monitoring stack
- [ ] Accessed Grafana dashboard
- [ ] Reviewed security overview
- [ ] Created test alert
- [ ] Generated sample report
- [ ] Understood API endpoints
- [ ] Reviewed compliance status
- [ ] Investigated sample incident
- [ ] Read key documentation
- [ ] Joined team Slack channel
- [ ] Scheduled mentoring session
- [ ] Created personal dashboard

---

**Document Version**: 1.0
**Last Updated**: 2024-01-15
**Status**: Ready for Use ✅
