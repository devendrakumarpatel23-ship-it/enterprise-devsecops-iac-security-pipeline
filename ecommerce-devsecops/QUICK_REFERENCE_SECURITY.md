# 🔒 Enterprise Security Platform - Quick Reference

## 📋 Module Overview

| Module | Purpose | Language | Key Files |
|--------|---------|----------|-----------|
| **SOC Dashboard** | Real-time security visualization | React/JS | `frontend/src/pages/SecurityDashboard.js` |
| **Risk Engine** | AI-powered risk scoring | Python | `backend/app/security/ai_risk_engine.py` |
| **Alert Manager** | Real-time threat alerting | Python | `backend/app/security/alert_manager.py` |
| **MITRE Mapping** | Attack pattern analysis | Python | `backend/app/security/mitre_attack_engine.py` |
| **Compliance** | Multi-framework validation | Python | `backend/app/security/compliance_validator.py` |
| **CI/CD Gates** | Deployment security checks | YAML | `.github/workflows/advanced-security-gates.yml` |
| **Zero Trust** | Trust validation | Python | `backend/app/security/zero_trust_validator.py` |
| **Reports** | Export and visualization | Python | `backend/app/security/report_generator.py` |
| **Vulnerability Prioritizer** | Risk triage | Python | `backend/app/security/vulnerability_prioritizer.py` |
| **Monitoring Stack** | Infrastructure monitoring | Docker/YAML | `monitoring/docker-compose.yml` |

---

## 🚀 Quick Start Commands

```bash
# Deploy monitoring stack
cd monitoring && docker-compose up -d && cd ..

# Access Grafana
open http://localhost:3000
# Username: admin
# Password: SecurePassword123!

# View Prometheus metrics
open http://localhost:9090

# View Kibana logs
open http://localhost:5601

# Deploy security platform
bash scripts/deploy-security-platform.sh
```

---

## 🔧 Configuration Quick Links

| Component | Config File | Port | Purpose |
|-----------|------------|------|---------|
| Prometheus | `monitoring/prometheus/prometheus.yml` | 9090 | Metrics collection |
| Grafana | `monitoring/grafana/dashboards/` | 3000 | Dashboards |
| Elasticsearch | `monitoring/elk/elasticsearch/elasticsearch.yml` | 9200 | Log storage |
| Kibana | `monitoring/elk/kibana/kibana.yml` | 5601 | Log visualization |
| Logstash | `monitoring/elk/logstash/pipeline/logstash.conf` | 5000 | Log processing |

---

## 📊 Dashboard Access

| Dashboard | URL | Purpose |
|-----------|-----|---------|
| Grafana SOC | http://localhost:3000 | Main security dashboard |
| Prometheus UI | http://localhost:9090 | Raw metrics browser |
| Kibana | http://localhost:5601 | Log search & analysis |
| AlertManager | http://localhost:9093 | Alert routing |

---

## 🔐 API Endpoints Quick Reference

```bash
# Dashboard overview
GET /api/security/overview

# List vulnerabilities
GET /api/security/vulnerabilities?priority=CRITICAL&limit=10

# Get specific CVE details
GET /api/security/vulnerabilities/CVE-2024-1234

# Current risk score
GET /api/security/risk-score

# AI recommendations
GET /api/security/recommendations?limit=5

# Compliance status
GET /api/security/compliance-status

# MITRE ATT&CK matrix
GET /api/security/mitre-matrix

# Threat events (real-time)
GET /api/security/threat-events

# Trends (last 7 days)
GET /api/security/trends?days=7

# KPI metrics
GET /api/security/kpi-metrics

# Download reports
GET /api/security/report/download?format=json

# Health check
GET /api/security/health
```

---

## 📈 Key Metrics Definitions

| Metric | Definition | Range | Status |
|--------|-----------|-------|--------|
| **Security Score** | Overall security posture | 0-100 | >85 = Good |
| **Risk Score** | Organizational risk level | 0-100 | <35 = Good |
| **Compliance Score** | Framework compliance | 0-100% | >85% = Good |
| **MTTD** | Mean Time to Detect | Hours | <2h = Good |
| **MTTR** | Mean Time to Respond | Hours | <4h = Good |
| **Patch Rate** | Monthly patching % | % | >90% = Good |

---

## 🎯 Alert Severity Levels

| Level | Color | Response Time | Example |
|-------|-------|----------------|---------|
| CRITICAL | 🔴 Red | Immediate | RCE detected, active data exfil |
| HIGH | 🟠 Orange | 1 hour | CVE 7.0+, privilege escalation |
| MEDIUM | 🟡 Yellow | 4 hours | CVE 5.0-6.9, policy violation |
| LOW | 🟢 Green | 24 hours | Information gathering |
| INFO | ⚪ White | 1 week | Configuration updates |

---

## 🔄 Workflow Examples

### Responding to Critical Alert
1. Alert triggers in Grafana/AlertManager
2. Slack notification sent to team
3. Auto-create incident ticket
4. Execute incident response playbook
5. Gather forensic data
6. Contain threat
7. Remediate vulnerability
8. Verify fix
9. Close incident
10. Review lessons learned

### Processing New CVE
1. CVE appears in vulnerability feed
2. Risk engine calculates score
3. MITRE mapping auto-generated
4. Compliance impact assessed
5. Prioritization determined
6. Recommendation created
7. Dashboard alert triggered
8. Remediation roadmap built
9. SLA assigned
10. Teams notified

---

## 📝 Report Types

| Report Type | Format | Use Case |
|-------------|--------|----------|
| **Security Report** | JSON | Data analysis & automation |
| **Executive Summary** | JSON | Leadership briefings |
| **Compliance Report** | JSON | Audit readiness |
| **Risk Assessment** | JSON | Risk quantification |
| **HTML Dashboard** | HTML | Executive review |
| **PDF Export** | HTML→PDF | Regulatory submission |

---

## 🛠️ Customization Guide

### Add Custom Dashboard Panel
1. Edit `monitoring/grafana/dashboards/security-soc-dashboard.json`
2. Add new panel object with Prometheus query
3. Restart Grafana
4. Verify panel appears

### Add Custom Alert Rule
1. Edit `monitoring/prometheus/alert.rules.yml`
2. Add alert rule with PromQL expression
3. Restart Prometheus
4. Test alert firing

### Add Custom Python Security Module
1. Create new file in `backend/app/security/`
2. Implement security checks
3. Export via REST API
4. Add dashboard integration

---

## 🐛 Troubleshooting

### Grafana Dashboard Not Loading
```bash
# Check service status
docker-compose logs grafana

# Restart service
docker-compose restart grafana
```

### Prometheus Metrics Missing
```bash
# Check scrape targets
curl http://localhost:9090/api/v1/targets

# Verify alert rules
curl http://localhost:9090/api/v1/rules
```

### Elasticsearch Connection Issues
```bash
# Test connection
curl -X GET http://localhost:9200/

# Check cluster health
curl -X GET http://localhost:9200/_cluster/health
```

---

## 📚 Documentation Links

| Document | Location | Purpose |
|----------|----------|---------|
| Advanced Features | `ADVANCED_SECURITY_FEATURES.md` | Detailed feature docs |
| Implementation Summary | `IMPLEMENTATION_SUMMARY.md` | Complete overview |
| API Documentation | `docs/API.md` | API reference |
| Deployment Guide | `docs/DEPLOYMENT.md` | Deployment steps |
| Security Policy | `SECURITY.md` | Security guidelines |

---

## 👥 Team Responsibilities

| Role | Dashboard | Key Metrics | Actions |
|------|-----------|------------|---------|
| **Security Lead** | Overview | Risk Score, MTTD | Strategic decisions |
| **SOC Analyst** | Alerts | Incident timeline | Investigation |
| **DevOps** | CI/CD | Deployment success | Gate approval |
| **Compliance** | Compliance | Framework scores | Audit prep |
| **CTO** | Executive | Security posture | Roadmap planning |

---

## 🔔 Notification Channels

| Channel | Use | Example |
|---------|-----|---------|
| **Email** | High priority | Critical CVE alert |
| **Slack** | Real-time | Threat detected |
| **PagerDuty** | On-call escalation | CRITICAL alert |
| **Webhook** | Integration | Custom systems |
| **Ticket** | Tracking | Audit trail |

---

## 📊 Compliance Frameworks Quick Reference

| Framework | Key Controls | Primary Focus |
|-----------|--------------|---------------|
| **PCI-DSS** | 12 requirements | Payment security |
| **OWASP Top 10** | 10 vulnerabilities | Web security |
| **CIS** | 20+ controls | Best practices |
| **NIST CSF** | 5 functions | Cybersecurity |
| **SOC 2** | 8 criteria | Trust services |
| **ISO 27001** | 100+ controls | Information security |

---

## 🎨 UI Navigation Guide

### Dashboard Sections
1. **Header** - Title, refresh rate
2. **KPI Cards** - Real-time metrics
3. **Tab Navigation** - Overview, Vulns, Threats, Compliance, Recommendations
4. **Charts** - CVE trends, threat distribution
5. **Alerts** - Priority-sorted list
6. **Recommendations** - AI suggestions

### Keyboard Shortcuts
- `Ctrl+Shift+D` - Jump to Dashboard
- `Ctrl+Alt+A` - View Alerts
- `Ctrl+Alt+R` - Generate Report
- `?` - Help menu

---

## 🔐 Security Best Practices

### Dashboard Access
- ✅ Use SSO/OIDC
- ✅ Enable 2FA on admin accounts
- ✅ Regular password rotation
- ✅ Audit access logs
- ✅ Principle of least privilege

### Data Protection
- ✅ Encrypt in transit (TLS 1.3)
- ✅ Encrypt at rest (AES-256)
- ✅ Regular backups
- ✅ Data retention policy
- ✅ Secure deletion procedures

### API Security
- ✅ API key rotation
- ✅ Rate limiting
- ✅ Request signing
- ✅ Audit all API calls
- ✅ Use OAuth 2.0

---

## 📞 Support Resources

**Email**: security@enterprise.com
**Slack**: #security-platform
**Wiki**: https://wiki.enterprise.com/security
**Issues**: GitHub Issues
**Documentation**: docs/ folder

---

## 📋 Maintenance Checklist

- [ ] Daily: Check dashboard
- [ ] Daily: Review critical alerts
- [ ] Weekly: Analyze trends
- [ ] Weekly: Update vulnerability feeds
- [ ] Monthly: Security review
- [ ] Monthly: Compliance audit
- [ ] Quarterly: Penetration test
- [ ] Quarterly: Policy review
- [ ] Annually: Disaster recovery drill

---

**Last Updated**: 2024-01-15
**Version**: 1.0.0
**Status**: Production ✅
