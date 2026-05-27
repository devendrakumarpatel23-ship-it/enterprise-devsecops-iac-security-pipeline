"""
Alert Manager & Real-time Security Alerting System
Handles runtime security alerts, intrusion detection, and anomaly alerts
"""
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
from enum import Enum
from dataclasses import dataclass, asdict


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class AlertCategory(Enum):
    """Alert categories"""
    INTRUSION_DETECTION = "intrusion_detection"
    CONTAINER_ANOMALY = "container_anomaly"
    AUTHENTICATION_FAILURE = "authentication_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_EXFILTRATION = "data_exfiltration"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    MALWARE_DETECTION = "malware_detection"
    POLICY_VIOLATION = "policy_violation"
    COMPLIANCE_BREACH = "compliance_breach"
    PERFORMANCE_ANOMALY = "performance_anomaly"


@dataclass
class SecurityAlert:
    """Represents a security alert"""
    alert_id: str
    timestamp: str
    category: str
    severity: str
    source_system: str
    description: str
    affected_resource: str
    indicator_of_compromise: List[str]
    recommended_action: str
    status: str = "open"
    investigation_notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class RuntimeSecurityMonitor:
    """Monitors runtime security events and generates alerts"""

    def __init__(self):
        self.alerts: List[SecurityAlert] = []
        self.event_log: List[Dict] = []
        self.closed_alerts: List[SecurityAlert] = []

    def detect_unauthorized_access(
        self, source_ip: str, target_resource: str, user_id: str = None
    ) -> SecurityAlert:
        """Detect unauthorized API/resource access"""
        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.UNAUTHORIZED_ACCESS.value,
            severity=AlertSeverity.HIGH.name,
            source_system="api-gateway",
            description=f"Unauthorized access attempt to {target_resource} from {source_ip}",
            affected_resource=target_resource,
            indicator_of_compromise=[
                source_ip,
                target_resource,
                f"user_{user_id}" if user_id else "anonymous",
            ],
            recommended_action="Block IP address and review access logs",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def detect_failed_login_attempts(
        self, username: str, source_ip: str, attempt_count: int = 5
    ) -> SecurityAlert:
        """Detect multiple failed login attempts"""
        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.AUTHENTICATION_FAILURE.value,
            severity=AlertSeverity.MEDIUM.name if attempt_count < 10 else AlertSeverity.HIGH.name,
            source_system="auth-service",
            description=f"{attempt_count} failed login attempts for user '{username}' from {source_ip}",
            affected_resource=f"user:{username}",
            indicator_of_compromise=[source_ip, username],
            recommended_action="Lock account and notify user. Investigate for credential compromise.",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def detect_container_anomaly(
        self, container_id: str, anomaly_type: str, severity: AlertSeverity = AlertSeverity.HIGH
    ) -> SecurityAlert:
        """Detect container runtime anomalies"""
        anomaly_descriptions = {
            "escape_attempt": "Container escape attempt detected",
            "privilege_escalation": "Privilege escalation detected within container",
            "resource_exhaustion": "Unusual resource consumption detected",
            "network_anomaly": "Unusual network traffic from container",
            "process_injection": "Process injection detected",
        }

        description = anomaly_descriptions.get(anomaly_type, "Unknown container anomaly")

        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.CONTAINER_ANOMALY.value,
            severity=severity.name,
            source_system="container-runtime",
            description=f"{description} in container {container_id}",
            affected_resource=f"container:{container_id}",
            indicator_of_compromise=[container_id, anomaly_type],
            recommended_action=f"Immediately isolate container {container_id} and investigate. Consider terminating if confirmed malicious.",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def detect_intrusion_signature(
        self, signature_name: str, source_ip: str, target_host: str, protocol: str
    ) -> SecurityAlert:
        """Detect intrusion based on known signatures"""
        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.INTRUSION_DETECTION.value,
            severity=AlertSeverity.CRITICAL.name,
            source_system="ids-system",
            description=f"Intrusion signature detected: {signature_name} from {source_ip} to {target_host} via {protocol}",
            affected_resource=target_host,
            indicator_of_compromise=[source_ip, target_host, signature_name, protocol],
            recommended_action="Activate incident response procedure. Block attacker IP. Preserve forensic evidence.",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def detect_data_exfiltration(
        self, source_system: str, data_size_mb: float, destination_ip: str
    ) -> SecurityAlert:
        """Detect suspicious data exfiltration"""
        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.DATA_EXFILTRATION.value,
            severity=AlertSeverity.CRITICAL.name,
            source_system="dlp-system",
            description=f"Large data transfer detected: {data_size_mb}MB from {source_system} to {destination_ip}",
            affected_resource=source_system,
            indicator_of_compromise=[source_system, destination_ip, f"{data_size_mb}MB"],
            recommended_action="Immediately block outbound connection. Investigate for data breach. Notify security team.",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def detect_privilege_escalation(
        self, user_id: str, from_privilege: str, to_privilege: str, method: str
    ) -> SecurityAlert:
        """Detect unauthorized privilege escalation"""
        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.PRIVILEGE_ESCALATION.value,
            severity=AlertSeverity.CRITICAL.name,
            source_system="audit-system",
            description=f"Privilege escalation detected: {user_id} escalated from {from_privilege} to {to_privilege} via {method}",
            affected_resource=f"user:{user_id}",
            indicator_of_compromise=[user_id, method, to_privilege],
            recommended_action="Revoke elevated privileges. Audit user activity. Review authorization policies.",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def detect_malware_signature(
        self, file_path: str, malware_name: str, file_hash: str
    ) -> SecurityAlert:
        """Detect malware based on signature"""
        alert = SecurityAlert(
            alert_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            category=AlertCategory.MALWARE_DETECTION.value,
            severity=AlertSeverity.CRITICAL.name,
            source_system="antivirus-system",
            description=f"Malware detected: {malware_name} at {file_path}",
            affected_resource=file_path,
            indicator_of_compromise=[file_hash, malware_name, file_path],
            recommended_action="Isolate system immediately. Quarantine file. Run full system scan. Check for lateral movement.",
        )
        self.alerts.append(alert)
        self._log_event(alert)
        return alert

    def _log_event(self, alert: SecurityAlert):
        """Log alert event"""
        self.event_log.append(
            {
                "timestamp": alert.timestamp,
                "alert_id": alert.alert_id,
                "category": alert.category,
                "severity": alert.severity,
            }
        )

    def close_alert(self, alert_id: str, resolution_notes: str = "") -> bool:
        """Close an alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.status = "closed"
                alert.investigation_notes = resolution_notes
                self.closed_alerts.append(alert)
                self.alerts.remove(alert)
                return True
        return False

    def get_open_alerts(self, severity_filter: str = None) -> List[Dict]:
        """Get all open alerts"""
        alerts = self.alerts
        if severity_filter:
            alerts = [a for a in alerts if a.severity == severity_filter]
        return [a.to_dict() for a in sorted(
            alerts, key=lambda x: AlertSeverity[x.severity].value, reverse=True
        )]

    def get_alerts_by_category(self, category: str) -> List[Dict]:
        """Get alerts filtered by category"""
        return [a.to_dict() for a in self.alerts if a.category == category]

    def get_alert_timeline(self, hours: int = 24) -> List[Dict]:
        """Get alert timeline for specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        timeline = []

        for alert in self.alerts:
            alert_time = datetime.fromisoformat(alert.timestamp)
            if alert_time > cutoff:
                timeline.append(alert.to_dict())

        return sorted(timeline, key=lambda x: x["timestamp"], reverse=True)

    def generate_incident_report(self, alert_id: str) -> Dict:
        """Generate detailed incident report"""
        alert = None
        for a in self.alerts + self.closed_alerts:
            if a.alert_id == alert_id:
                alert = a
                break

        if not alert:
            return {"error": "Alert not found"}

        return {
            "alert_id": alert.alert_id,
            "incident_report": {
                "timestamp": alert.timestamp,
                "category": alert.category,
                "severity": alert.severity,
                "description": alert.description,
                "affected_resource": alert.affected_resource,
                "indicators": alert.indicator_of_compromise,
                "recommended_actions": alert.recommended_action,
                "investigation_status": alert.status,
                "notes": alert.investigation_notes,
            },
        }

    def export_alerts_log(self, filepath: str) -> bool:
        """Export alerts to log file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "open_alerts": self.get_open_alerts(),
                "closed_alerts": [a.to_dict() for a in self.closed_alerts],
                "event_log": self.event_log,
                "statistics": {
                    "total_alerts": len(self.alerts) + len(self.closed_alerts),
                    "open_count": len(self.alerts),
                    "critical_count": sum(1 for a in self.alerts if a.severity == "CRITICAL"),
                    "high_count": sum(1 for a in self.alerts if a.severity == "HIGH"),
                },
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting alerts: {e}")
            return False


# Initialize monitor and create sample alerts
def create_sample_security_events(monitor: RuntimeSecurityMonitor):
    """Generate sample security events for demonstration"""
    monitor.detect_unauthorized_access(
        source_ip="192.168.1.100",
        target_resource="/api/admin/users",
        user_id="user_123",
    )

    monitor.detect_failed_login_attempts(
        username="admin@example.com",
        source_ip="10.0.0.50",
        attempt_count=7,
    )

    monitor.detect_container_anomaly(
        container_id="container_abc123",
        anomaly_type="escape_attempt",
        severity=AlertSeverity.CRITICAL,
    )

    monitor.detect_intrusion_signature(
        signature_name="SQL_INJECTION_ATTEMPT_001",
        source_ip="203.0.113.45",
        target_host="api-server-01",
        protocol="HTTPS",
    )

    monitor.detect_data_exfiltration(
        source_system="database-01",
        data_size_mb=2500.5,
        destination_ip="198.51.100.20",
    )

    monitor.detect_privilege_escalation(
        user_id="user_456",
        from_privilege="user",
        to_privilege="root",
        method="kernel_exploit",
    )

    monitor.detect_malware_signature(
        file_path="/opt/app/suspicious_binary",
        malware_name="Trojan.Generic.001",
        file_hash="a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    )


if __name__ == "__main__":
    monitor = RuntimeSecurityMonitor()
    create_sample_security_events(monitor)

    print("Open Alerts:")
    for alert in monitor.get_open_alerts():
        print(f"  [{alert['severity']}] {alert['description']}")

    print("\nAlert Statistics:")
    print(f"  Total Open: {len(monitor.get_open_alerts())}")
    print(f"  Critical: {len(monitor.get_open_alerts('CRITICAL'))}")
    print(f"  High: {len(monitor.get_open_alerts('HIGH'))}")

    monitor.export_alerts_log("security_alerts.json")
    print("\nAlerts exported to security_alerts.json")
