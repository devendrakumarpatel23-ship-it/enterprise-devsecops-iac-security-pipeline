"""
Enterprise SOC / Cyber Defense War Room Simulator
Simulates realistic Security Operations Center with live threats, incidents, and responses
Inspired by Microsoft Sentinel, Splunk, CrowdStrike Falcon, IBM QRadar, Palo Alto Cortex XDR
"""

import json
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import uuid


class ThreatSeverity(Enum):
    """Threat severity levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class IncidentStatus(Enum):
    """Incident response status"""
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    REMEDIATED = "remediated"
    RESOLVED = "resolved"


class AttackType(Enum):
    """Types of attacks in MITRE ATT&CK framework"""
    SQL_INJECTION = "T1190"  # Exploit Public-Facing Application
    XSS_ATTACK = "T1598"  # Phishing: Search Open Websites
    BRUTE_FORCE = "T1110"  # Brute Force
    API_ABUSE = "T1550"  # Use Alternate Authentication Material
    PORT_SCANNING = "T1046"  # Network Service Discovery
    CONTAINER_ESCAPE = "T1611"  # Escape to Host
    PRIVILEGE_ESCALATION = "T1548"  # Abuse Elevation Control Mechanism
    LATERAL_MOVEMENT = "T1570"  # Lateral Tool Transfer
    PERSISTENCE = "T1098"  # Account Manipulation
    DEFENSE_EVASION = "T1562"  # Impair Defenses


class MITREATTACKMapping:
    """MITRE ATT&CK Framework mapping"""
    TACTICS = {
        "reconnaissance": "Information Gathering",
        "initial_access": "Initial Access",
        "execution": "Code Execution",
        "persistence": "Maintains Access",
        "privilege_escalation": "Elevate Privileges",
        "defense_evasion": "Evade Detection",
        "credential_access": "Steal Credentials",
        "discovery": "Enumerate Environment",
        "lateral_movement": "Move Laterally",
        "collection": "Gather Data",
        "exfiltration": "Steal Data",
        "command_and_control": "Command & Control",
        "impact": "Destructive",
    }

    MITIGATIONS = {
        "T1190": ["WAF", "IDS/IPS", "Input Validation"],
        "T1598": ["Security Awareness", "Email Filtering"],
        "T1110": ["MFA", "Account Lockout Policy", "Rate Limiting"],
        "T1550": ["MFA", "Network Segmentation", "Log Monitoring"],
        "T1046": ["Network Segmentation", "Firewall Rules"],
        "T1611": ["Container Runtime Security", "Network Policies"],
        "T1548": ["Privilege Escalation Prevention", "RBAC"],
        "T1570": ["Network Segmentation", "EDR"],
        "T1098": ["MFA", "Account Monitoring"],
        "T1562": ["Immutable Logs", "SIEM Monitoring"],
    }


@dataclass
class SecurityEvent:
    """Represents a single security event"""
    event_id: str
    timestamp: datetime
    source_ip: str
    target: str
    event_type: str
    severity: ThreatSeverity
    description: str
    mitre_attack_id: str
    affected_asset: str
    metadata: Dict


@dataclass
class SecurityAlert:
    """Represents a correlated security alert"""
    alert_id: str
    timestamp: datetime
    title: str
    description: str
    severity: ThreatSeverity
    attack_type: AttackType
    mitre_attack_id: str
    event_count: int
    source_ips: List[str]
    target_systems: List[str]
    affected_users: List[str]
    confidence_score: float
    status: str


@dataclass
class Incident:
    """Represents a security incident"""
    incident_id: str
    created_at: datetime
    severity: ThreatSeverity
    title: str
    description: str
    attack_type: AttackType
    mitre_tactic: str
    status: IncidentStatus
    alerts: List[str]
    affected_systems: List[str]
    affected_users: List[str]
    root_cause: Optional[str]
    remediation_actions: List[str]
    investigation_notes: List[Dict]
    timeline: List[Dict]
    impact_assessment: Dict
    assigned_analyst: Optional[str]
    sla_breach: bool


class SOCSimulator:
    """Enterprise SOC simulation engine"""

    def __init__(self):
        self.events: List[SecurityEvent] = []
        self.alerts: List[SecurityAlert] = []
        self.incidents: Dict[str, Incident] = {}
        self.threat_score = 0.0
        self.security_posture = 85.0
        self.active_threats = []
        self.threat_timeline = []
        self.organization_assets = self._initialize_assets()
        self.threat_actors = self._initialize_threat_actors()
        self.generate_baseline_events()

    def _initialize_assets(self) -> Dict:
        """Initialize organization assets"""
        return {
            "databases": ["prod-db-01", "prod-db-02", "cache-redis-01", "analytics-db"],
            "servers": ["web-server-01", "web-server-02", "api-gateway", "auth-server"],
            "containers": ["container-1", "container-2", "container-3", "worker-pod-1"],
            "kubernetes_clusters": ["prod-cluster", "staging-cluster"],
            "networks": ["internal-net-10.0", "dmz-net-192.168", "vpn-net-172.16"],
            "endpoints": [f"endpoint-{i}" for i in range(1, 11)],
            "applications": ["ecommerce-app", "api-service", "worker-service", "admin-panel"],
        }

    def _initialize_threat_actors(self) -> List[Dict]:
        """Initialize threat actor profiles"""
        return [
            {
                "name": "APT-28",
                "sophistication": 0.95,
                "motive": "Espionage",
                "attacks": ["T1110", "T1570", "T1098"],
            },
            {
                "name": "FIN7",
                "sophistication": 0.90,
                "motive": "Financial",
                "attacks": ["T1190", "T1598", "T1110"],
            },
            {
                "name": "Lazarus",
                "sophistication": 0.92,
                "motive": "Financial/Disruption",
                "attacks": ["T1611", "T1548", "T1190"],
            },
            {
                "name": "Internal Threat",
                "sophistication": 0.60,
                "motive": "Malice/Negligence",
                "attacks": ["T1550", "T1098"],
            },
        ]

    def generate_baseline_events(self):
        """Generate baseline security events for context"""
        now = datetime.now()
        for i in range(15):
            self._create_event(
                now - timedelta(minutes=random.randint(1, 300)),
                "normal_activity",
                ThreatSeverity.INFO,
            )

    def _create_event(
        self,
        timestamp: datetime,
        event_type: str,
        severity: ThreatSeverity,
        metadata: Optional[Dict] = None,
    ) -> SecurityEvent:
        """Create a security event"""
        event_types_config = {
            "normal_activity": {
                "desc": "Normal user activity",
                "sources": ["user-{i}".format(i=random.randint(1, 100))],
                "targets": random.choices(self.organization_assets["servers"], k=1),
                "mitre": "T1552",
            },
            "failed_login": {
                "desc": "Failed login attempt",
                "sources": [f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"],
                "targets": ["auth-server"],
                "mitre": "T1110",
            },
            "sql_injection": {
                "desc": "SQL Injection attempt detected",
                "sources": [f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"],
                "targets": ["prod-db-01"],
                "mitre": "T1190",
            },
            "xss_attack": {
                "desc": "XSS attack detected in API request",
                "sources": [f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"],
                "targets": ["api-gateway"],
                "mitre": "T1598",
            },
            "port_scan": {
                "desc": "Port scanning activity detected",
                "sources": [f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"],
                "targets": ["internal-net-10.0"],
                "mitre": "T1046",
            },
            "unauthorized_access": {
                "desc": "Unauthorized API access attempt",
                "sources": ["internal-user-123"],
                "targets": ["api-gateway"],
                "mitre": "T1550",
            },
        }

        config = event_types_config.get(event_type, event_types_config["normal_activity"])
        source_ip = random.choice(config["sources"])
        target = random.choice(config["targets"])

        event = SecurityEvent(
            event_id=str(uuid.uuid4()),
            timestamp=timestamp,
            source_ip=source_ip,
            target=target,
            event_type=event_type,
            severity=severity,
            description=config["desc"],
            mitre_attack_id=config["mitre"],
            affected_asset=target,
            metadata=metadata or {},
        )

        self.events.append(event)
        return event

    def generate_attack_simulation(self) -> Tuple[List[SecurityEvent], List[SecurityAlert]]:
        """Generate realistic attack simulation"""
        now = datetime.now()
        attack_type = random.choice(list(AttackType))
        threat_actor = random.choice(self.threat_actors)
        num_events = random.randint(5, 20)

        events = []
        for i in range(num_events):
            event = self._create_event(
                now - timedelta(seconds=random.randint(1, 60)),
                attack_type.name.lower(),
                random.choice([ThreatSeverity.HIGH, ThreatSeverity.CRITICAL]),
            )
            events.append(event)

        # Correlate events into alerts
        alerts = self._correlate_events(events, attack_type, threat_actor)
        self.active_threats.append({
            "type": attack_type.name,
            "actor": threat_actor["name"],
            "severity": alerts[0].severity.name if alerts else "UNKNOWN",
            "detected_at": now.isoformat(),
            "event_count": len(events),
        })

        return events, alerts

    def _correlate_events(
        self,
        events: List[SecurityEvent],
        attack_type: AttackType,
        threat_actor: Dict,
    ) -> List[SecurityAlert]:
        """Correlate events into alerts"""
        alerts = []
        source_ips = list(set([e.source_ip for e in events]))
        targets = list(set([e.target for e in events]))

        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            title=f"Potential {attack_type.name.replace('_', ' ')} Attack",
            description=f"Multiple events correlating to {attack_type.name} attack chain from {threat_actor['name']}",
            severity=ThreatSeverity.CRITICAL if len(events) > 10 else ThreatSeverity.HIGH,
            attack_type=attack_type,
            mitre_attack_id=attack_type.value,
            event_count=len(events),
            source_ips=source_ips,
            target_systems=targets,
            affected_users=self._extract_affected_users(events),
            confidence_score=min(0.95, 0.5 + len(events) * 0.05),
            status="triggered",
        )

        alerts.append(alert)
        self.alerts.append(alert)
        return alerts

    def _extract_affected_users(self, events: List[SecurityEvent]) -> List[str]:
        """Extract affected users from events"""
        users = []
        for event in events:
            if "user-" in event.source_ip:
                users.append(event.source_ip)
        return users or ["unknown-user"]

    def create_incident_from_alert(self, alert: SecurityAlert) -> Incident:
        """Create incident from alert"""
        incident = Incident(
            incident_id=str(uuid.uuid4()),
            created_at=datetime.now(),
            severity=alert.severity,
            title=f"Incident: {alert.title}",
            description=alert.description,
            attack_type=alert.attack_type,
            mitre_tactic=random.choice(list(MITREATTACKMapping.TACTICS.keys())),
            status=IncidentStatus.DETECTED,
            alerts=[alert.alert_id],
            affected_systems=alert.target_systems,
            affected_users=alert.affected_users,
            root_cause=None,
            remediation_actions=[],
            investigation_notes=[
                {
                    "timestamp": datetime.now().isoformat(),
                    "analyst": "SOC-AI",
                    "note": "Initial detection and correlation completed",
                }
            ],
            timeline=[
                {
                    "time": datetime.now().isoformat(),
                    "event": "Incident created from alert correlation",
                    "severity": alert.severity.name,
                }
            ],
            impact_assessment={
                "data_exposure": random.choice([True, False]),
                "systems_affected": len(alert.target_systems),
                "users_affected": len(alert.affected_users),
                "estimated_impact": f"${random.randint(10000, 500000)}",
            },
            assigned_analyst=random.choice(["Alice Chen", "Bob Smith", "Carol Davis"]),
            sla_breach=False,
        )

        self.incidents[incident.incident_id] = incident
        return incident

    def update_incident_status(
        self, incident_id: str, new_status: IncidentStatus, notes: str = ""
    ) -> Optional[Incident]:
        """Update incident status"""
        if incident_id not in self.incidents:
            return None

        incident = self.incidents[incident_id]
        incident.status = new_status

        if notes:
            incident.investigation_notes.append({
                "timestamp": datetime.now().isoformat(),
                "analyst": "SOC-Human",
                "note": notes,
            })

        incident.timeline.append({
            "time": datetime.now().isoformat(),
            "event": f"Status changed to {new_status.value}",
            "severity": incident.severity.name,
        })

        return incident

    def add_remediation_action(
        self, incident_id: str, action: str
    ) -> Optional[Incident]:
        """Add remediation action to incident"""
        if incident_id not in self.incidents:
            return None

        incident = self.incidents[incident_id]
        incident.remediation_actions.append(action)
        return incident

    def calculate_threat_score(self) -> float:
        """Calculate overall threat score"""
        critical_count = sum(1 for a in self.alerts if a.severity == ThreatSeverity.CRITICAL)
        high_count = sum(1 for a in self.alerts if a.severity == ThreatSeverity.HIGH)
        incident_count = len(self.incidents)

        threat_score = (critical_count * 25) + (high_count * 15) + (incident_count * 10)
        self.threat_score = min(100, threat_score)
        return self.threat_score

    def calculate_security_posture(self) -> float:
        """Calculate security posture score (inverse of threat)"""
        threat_score = self.calculate_threat_score()
        self.security_posture = max(0, 100 - threat_score)
        return self.security_posture

    def get_threat_heatmap(self) -> Dict:
        """Generate threat heatmap data"""
        heatmap = {}
        for asset_type, assets in self.organization_assets.items():
            heatmap[asset_type] = []
            for asset in assets[:5]:  # Limit for visualization
                threat_level = random.uniform(0, 100)
                heatmap[asset_type].append({
                    "name": asset,
                    "threat_level": threat_level,
                    "events": random.randint(0, 50),
                })
        return heatmap

    def get_dashboard_data(self) -> Dict:
        """Get comprehensive SOC dashboard data"""
        return {
            "timestamp": datetime.now().isoformat(),
            "threat_score": self.calculate_threat_score(),
            "security_posture": self.calculate_security_posture(),
            "active_alerts": len(self.alerts),
            "critical_alerts": sum(
                1 for a in self.alerts if a.severity == ThreatSeverity.CRITICAL
            ),
            "open_incidents": sum(
                1 for i in self.incidents.values()
                if i.status not in [IncidentStatus.RESOLVED, IncidentStatus.REMEDIATED]
            ),
            "recent_events": [asdict(e) for e in self.events[-10:]],
            "alerts": [asdict(a) for a in self.alerts[-20:]],
            "incidents": [asdict(i) for i in list(self.incidents.values())[-10:]],
            "active_threats": self.active_threats[-10:],
            "threat_heatmap": self.get_threat_heatmap(),
            "mitre_coverage": self._calculate_mitre_coverage(),
        }

    def _calculate_mitre_coverage(self) -> Dict:
        """Calculate MITRE ATT&CK coverage"""
        covered_tactics = set()
        for incident in self.incidents.values():
            covered_tactics.add(incident.mitre_tactic)

        return {
            "total_tactics": len(MITREATTACKMapping.TACTICS),
            "covered_tactics": len(covered_tactics),
            "coverage_percentage": (len(covered_tactics) / len(MITREATTACKMapping.TACTICS)) * 100,
            "tactics": list(covered_tactics),
        }

    def get_incident_queue(self) -> List[Dict]:
        """Get incident queue sorted by priority"""
        incidents = sorted(
            self.incidents.values(),
            key=lambda x: (x.severity.value, x.created_at),
            reverse=True,
        )
        return [asdict(i) for i in incidents]

    def get_threat_intelligence_summary(self) -> Dict:
        """Get AI threat intelligence summary"""
        return {
            "total_events_today": len(self.events),
            "total_alerts_today": len(self.alerts),
            "total_incidents": len(self.incidents),
            "top_attack_types": self._get_top_attack_types(),
            "top_threat_actors": self._get_top_threat_actors(),
            "recommended_actions": self._get_recommended_actions(),
            "ai_insights": self._generate_ai_insights(),
        }

    def _get_top_attack_types(self) -> List[Dict]:
        """Get top attack types by frequency"""
        attack_counts = {}
        for alert in self.alerts:
            key = alert.attack_type.name
            attack_counts[key] = attack_counts.get(key, 0) + 1

        return sorted(
            [{"type": k, "count": v} for k, v in attack_counts.items()],
            key=lambda x: x["count"],
            reverse=True,
        )[:5]

    def _get_top_threat_actors(self) -> List[Dict]:
        """Get top threat actors"""
        return sorted(self.threat_actors, key=lambda x: x["sophistication"], reverse=True)[:5]

    def _get_recommended_actions(self) -> List[str]:
        """Get AI-generated recommended actions"""
        recommendations = [
            "Implement MFA on all critical accounts",
            "Deploy WAF for API protection",
            "Enable container runtime security monitoring",
            "Increase network segmentation",
            "Deploy EDR on all endpoints",
            "Implement immutable logging",
            "Review and strengthen firewall rules",
        ]
        return random.sample(recommendations, min(3, len(recommendations)))

    def _generate_ai_insights(self) -> List[str]:
        """Generate AI-powered insights"""
        insights = [
            f"Detected {len(self.active_threats)} active threat patterns in last 24 hours",
            f"Security posture score: {self.security_posture:.1f}% - {self._get_posture_assessment()}",
            f"Critical alerts increased by {random.randint(10, 50)}% compared to yesterday",
            "Anomalous lateral movement detected in internal network",
            "Potential data exfiltration activity identified",
        ]
        return random.sample(insights, min(3, len(insights)))

    def _get_posture_assessment(self) -> str:
        """Get security posture assessment"""
        if self.security_posture >= 80:
            return "Strong"
        elif self.security_posture >= 60:
            return "Fair"
        elif self.security_posture >= 40:
            return "Weak"
        else:
            return "Critical"
