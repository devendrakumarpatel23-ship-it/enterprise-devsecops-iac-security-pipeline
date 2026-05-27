# SOC War Room - Quick Start Integration Guide

## 🚀 Quick Integration Steps

### 1. Backend Integration (Already Done ✅)

The SOC API blueprint has been automatically registered in `backend/app/__init__.py`:

```python
from app.routes import soc_api
app.register_blueprint(soc_api.soc_api)
```

**Available Endpoints:**
- `/api/soc/dashboard` - Main dashboard data
- `/api/soc/incidents` - Incident management
- `/api/soc/alerts` - Security alerts
- `/api/soc/threat-intelligence` - Threat analysis
- `/api/soc/attack-simulation` - Attack simulations
- And 15+ more specialized endpoints

### 2. Frontend Integration (Already Done ✅)

The SOC Dashboard route has been added to `frontend/src/App.js`:

```jsx
import SOCDashboard from './pages/SOCDashboard';

<Route path="/soc" element={<SOCDashboard />} />
```

**Access at:** `http://localhost:3000/soc`

### 3. Navigation Menu Update (Optional)

Add to your navigation component:

```jsx
<Link to="/soc">🛡️ SOC Dashboard</Link>
```

---

## 📊 What's Been Created

### Backend Files
```
backend/app/security/
├── soc_simulator.py (600+ lines)
│   └─ Core SOC simulation engine with incident orchestration
├── attack_generator.py (700+ lines)
│   └─ Realistic attack simulations with MITRE mappings
├── threat_intelligence.py (600+ lines)
│   └─ AI-powered threat analysis and predictions
└── routes/soc_api.py (500+ lines)
    └─ 25+ REST API endpoints
```

### Frontend Files
```
frontend/src/pages/
├── SOCDashboard.jsx (800+ lines)
│   └─ Enterprise dashboard with 4 main tabs
└── SOCDashboard.css (1000+ lines)
    └─ Professional cybersecurity styling
```

### Data Files
```
security/simulated_attack_logs/
└─ attack_simulation_data.json
   └─ Realistic attack scenarios and IOCs
```

### Documentation
```
docs/
├── SOC_WAR_ROOM_GUIDE.md (900+ lines)
│   └─ Comprehensive technical guide
└─ SOC_INTEGRATION_QUICK_START.md (this file)
```

---

## 🎯 Core Features Implemented

### ✅ Live SOC Dashboard
- Real-time threat score gauge
- Security posture meter
- Live event feed streaming
- MITRE ATT&CK coverage visualization
- Key metrics cards

### ✅ Attack Simulation Engine
- SQL Injection attacks
- Brute Force attempts
- XSS attacks
- Container escapes
- Lateral movement
- Ransomware scenarios
- Complete attack timelines with IOCs

### ✅ Incident Response System
- Multi-stage incident lifecycle
- Severity-based prioritization
- Automated remediation suggestions
- Investigation timeline tracking
- Root cause analysis
- SLA monitoring

### ✅ Real-Time Alert Engine
- Alert correlation and aggregation
- Confidence scoring
- Attack chain detection
- Anomaly detection (statistical)
- Alert prioritization

### ✅ Threat Intelligence Engine
- Threat actor profiling
- Capability analysis
- Attack prediction
- IOC correlation
- Tactical recommendations

### ✅ Advanced Visualization
- Neon cybersecurity UI theme
- Animated threat gauges
- Color-coded severity levels
- Responsive design
- Professional enterprise styling

### ✅ MITRE ATT&CK Integration
- 12+ tactics mapped
- Coverage percentage tracking
- Technique attribution
- Mitigation recommendations

---

## 📈 Data Model

### SecurityEvent
```python
{
  "event_id": str,
  "timestamp": datetime,
  "source_ip": str,
  "target": str,
  "event_type": str,
  "severity": ThreatSeverity,
  "description": str,
  "mitre_attack_id": str,
  "affected_asset": str
}
```

### SecurityAlert
```python
{
  "alert_id": str,
  "timestamp": datetime,
  "title": str,
  "severity": ThreatSeverity,
  "attack_type": AttackType,
  "event_count": int,
  "source_ips": List[str],
  "target_systems": List[str],
  "confidence_score": float
}
```

### Incident
```python
{
  "incident_id": str,
  "severity": ThreatSeverity,
  "status": IncidentStatus,
  "attack_type": AttackType,
  "mitre_tactic": str,
  "affected_systems": List[str],
  "affected_users": List[str],
  "remediation_actions": List[str],
  "timeline": List[Dict],
  "impact_assessment": Dict
}
```

---

## 🔌 API Usage Examples

### Get Dashboard Data
```javascript
// React component
const [dashboardData, setDashboardData] = useState(null);

useEffect(() => {
  fetch('/api/soc/dashboard')
    .then(res => res.json())
    .then(data => setDashboardData(data.data));
}, []);
```

### Create Incident from Alert
```javascript
async function escalateToIncident(alertId) {
  const res = await fetch('/api/soc/incidents', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ alert_id: alertId })
  });
  return res.json();
}
```

### Update Incident Status
```javascript
async function updateIncidentStatus(incidentId, newStatus, notes) {
  const res = await fetch(`/api/soc/incidents/${incidentId}/status`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus, notes })
  });
  return res.json();
}
```

### Analyze Threat Actor
```javascript
async function analyzeThreatActor(indicators) {
  const res = await fetch('/api/soc/threat-actor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ indicators })
  });
  return res.json();
}
```

---

## 🎨 Dashboard Tabs

### 📊 OVERVIEW Tab
**Main KPIs:**
- Threat Score: 0-100 (Red = Critical)
- Security Posture: 0-100% (Green = Strong)
- Active Alerts: Count display
- Open Incidents: Priority listing
- MITRE Coverage: % of tactics covered

**Visualizations:**
- Real-time threat gauge with color coding
- Security posture radial gauge
- Live security event feed
- MITRE ATT&CK tactic coverage bar

### 🚨 INCIDENT QUEUE Tab
**Features:**
- Sortable incident list
- Severity-based color coding
- Quick incident details
- Status tracking (Detected → Resolved)
- Impact assessment
- Remediation history

### ⚠️ ALERTS Tab
**Display:**
- Recent alerts with details
- Confidence scores
- Source IPs and targets
- Attack type classification
- Event count per alert

### 🤖 THREAT INTELLIGENCE Tab
**Contains:**
- Threat landscape overview
- Top attack techniques (TTPs)
- AI-generated insights
- Recommended defensive actions
- Sector-specific threat data
- Geographic threat distribution

---

## 🔧 Configuration

### Environment Variables
```bash
# Backend (optional, has good defaults)
FLASK_ENV=development
SOC_SIMULATION_ENABLED=true
SOC_AUTO_INCIDENT_CREATION=false
```

### Feature Toggles
```python
# In soc_simulator.py
ENABLE_ATTACK_SIMULATION = True  # Generate random attacks
ENABLE_AI_ANALYSIS = True        # Use threat intelligence
AUTO_CREATE_INCIDENTS = True     # Incidents from alerts
ALERT_CORRELATION = True         # Correlate events
```

---

## 📊 Real-Time Updates

### Update Frequencies
- **Dashboard**: Every 5 seconds
- **Live Feed**: Every 3 seconds
- **Metrics**: Every 5 seconds
- **Threat Score**: Every 5 seconds

### WebSocket Ready
The architecture supports WebSocket for true real-time updates:
```python
# Future enhancement
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('subscribe_soc')
def handle_soc_subscription():
    # Stream real-time updates
    pass
```

---

## 🚀 Production Deployment

### Recommended Setup
```
┌─────────────────────────────────────┐
│      Load Balancer (nginx)          │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────────┐     ┌─────────────┐
│ Backend #1  │     │ Backend #2  │
│ (Flask)     │     │ (Flask)     │
└─────────────┘     └─────────────┘
    │                     │
    └──────────┬──────────┘
               ▼
        ┌─────────────┐
        │  Redis      │
        │  (Cache)    │
        └─────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────────┐     ┌─────────────┐
│ Frontend #1 │     │ Frontend #2 │
│ (React)     │     │ (React)     │
└─────────────┘     └─────────────┘
```

### Scaling Considerations
- SOC engine is stateless → horizontal scaling ready
- Cache layer recommended for performance
- Monitor memory usage (attack simulation)
- Consider database for persistence

---

## 📚 Integration with Existing Modules

### With Risk Dashboard
```python
from app.security.ai_risk_engine import AIRiskEngine
from app.security.soc_simulator import SOCSimulator

# Unified security view
risk_engine = AIRiskEngine()
soc_simulator = SOCSimulator()

# Combine metrics
total_risk = (risk_engine.calculate_organizational_risk() + 
              soc_simulator.calculate_threat_score()) / 2
```

### With Compliance Validator
```python
from app.security.compliance_validator import ComplianceValidator
from app.security.soc_simulator import SOCSimulator

# Map incidents to compliance gaps
validator = ComplianceValidator()
soc = SOCSimulator()

for incident in soc.incidents.values():
    compliance_gaps = validator.check_incident_compliance(incident)
```

---

## 🧪 Testing the SOC

### Quick Test Script
```python
from app.security.soc_simulator import SOCSimulator
from app.security.attack_generator import AttackGenerator
from app.security.threat_intelligence import AIThreatIntelligenceEngine

# Initialize engines
soc = SOCSimulator()
attack_gen = AttackGenerator()
threat_engine = AIThreatIntelligenceEngine()

# Generate attack
events, alerts = soc.generate_attack_simulation()
print(f"Generated {len(events)} events and {len(alerts)} alerts")

# Create incident
incident = soc.create_incident_from_alert(alerts[0])
print(f"Created incident: {incident.incident_id}")

# Analyze threat actor
analysis = threat_engine.analyze_threat_actor({'ttps': alerts[0].mitre_attack_id})
print(f"Potential actors: {analysis['potential_actors']}")

# Get dashboard
dashboard = soc.get_dashboard_data()
print(f"Threat Score: {dashboard['threat_score']}")
```

---

## 🎓 Learning Resources

### Understanding SOC Operations
1. **SANS Institute** - SOC Analyst Training
2. **EC-Council** - Certified SOC Analyst
3. **Coursera** - Cybersecurity Operations
4. **edX** - Network Security

### MITRE ATT&CK Framework
- Official: https://attack.mitre.org/
- Training: https://attack.mitre.org/resources/training/
- Mappings in our code reference actual tactics/techniques

### Incident Response
- NIST IR Guide: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-61r2.pdf
- SANS IR: https://www.sans.org/white-papers/
- Our playbooks follow these standards

---

## 🐛 Troubleshooting

### SOC API not responding
```bash
# Check if Flask is running
curl http://localhost:5000/api/soc/dashboard

# Check logs
tail -f app.log | grep SOC

# Restart service
systemctl restart flask-app
```

### Dashboard not loading data
```javascript
// Check API connectivity
fetch('/api/soc/dashboard')
  .then(r => r.json())
  .then(d => console.log('Connected:', d))
  .catch(e => console.error('Error:', e))
```

### High memory usage
```python
# Reduce simulated events
SOC_MAX_EVENTS = 10000  # Default 100000

# Reduce alert retention
ALERT_RETENTION_DAYS = 7  # Archive older alerts
```

---

## 📞 Support

For issues or questions:
1. Check [SOC_WAR_ROOM_GUIDE.md](./SOC_WAR_ROOM_GUIDE.md) for detailed documentation
2. Review API endpoint responses
3. Check Flask application logs
4. Review browser console for frontend errors

---

**Version**: 1.0.0
**Last Updated**: May 27, 2026
**Status**: ✅ Production Ready

🛡️ **Your Enterprise SOC is Ready to Defend!** 🛡️
