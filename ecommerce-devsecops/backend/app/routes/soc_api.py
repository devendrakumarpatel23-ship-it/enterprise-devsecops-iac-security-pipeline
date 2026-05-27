"""
SOC War Room API Endpoints
REST API for enterprise security operations center
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import json
import random
from app.security.soc_simulator import SOCSimulator, IncidentStatus
from app.security.attack_generator import AttackGenerator
from app.security.threat_intelligence import AIThreatIntelligenceEngine

soc_api = Blueprint("soc_api", __name__, url_prefix="/api/soc")

# Initialize engines
soc_simulator = SOCSimulator()
attack_generator = AttackGenerator()
threat_engine = AIThreatIntelligenceEngine()


@soc_api.route("/dashboard", methods=["GET"])
def get_soc_dashboard():
    """Get comprehensive SOC dashboard data"""
    # Generate new attack simulation periodically
    if random.random() > 0.7:  # 30% chance to generate new attack
        events, alerts = soc_simulator.generate_attack_simulation()

    dashboard_data = soc_simulator.get_dashboard_data()

    return jsonify({
        "success": True,
        "data": dashboard_data,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/threat-score", methods=["GET"])
def get_threat_score():
    """Get current threat score"""
    return jsonify({
        "success": True,
        "threat_score": soc_simulator.calculate_threat_score(),
        "security_posture": soc_simulator.calculate_security_posture(),
        "risk_level": _get_risk_level(soc_simulator.threat_score),
        "trend": random.choice(["increasing", "decreasing", "stable"]),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/alerts", methods=["GET"])
def get_alerts():
    """Get security alerts"""
    limit = request.args.get("limit", default=20, type=int)
    severity = request.args.get("severity", default=None, type=str)

    alerts = soc_simulator.alerts[-limit:]

    if severity:
        alerts = [a for a in alerts if a.severity.name == severity]

    return jsonify({
        "success": True,
        "count": len(alerts),
        "alerts": [_serialize_alert(a) for a in alerts],
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/incidents", methods=["GET"])
def get_incidents():
    """Get security incidents"""
    limit = request.args.get("limit", default=50, type=int)
    status = request.args.get("status", default=None, type=str)

    incidents = soc_simulator.get_incident_queue()

    if status:
        incidents = [i for i in incidents if i["status"] == status]

    return jsonify({
        "success": True,
        "count": len(incidents),
        "incidents": incidents[:limit],
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/incidents", methods=["POST"])
def create_incident():
    """Create new incident from alert"""
    data = request.json
    alert_id = data.get("alert_id")

    # Find alert
    alert = next((a for a in soc_simulator.alerts if a.alert_id == alert_id), None)
    if not alert:
        return jsonify({"success": False, "error": "Alert not found"}), 404

    incident = soc_simulator.create_incident_from_alert(alert)

    return jsonify({
        "success": True,
        "incident": _serialize_incident(incident),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/incidents/<incident_id>", methods=["GET"])
def get_incident(incident_id):
    """Get incident details"""
    incident = soc_simulator.incidents.get(incident_id)

    if not incident:
        return jsonify({"success": False, "error": "Incident not found"}), 404

    return jsonify({
        "success": True,
        "incident": _serialize_incident(incident),
        "timeline": incident.timeline,
        "investigation_notes": incident.investigation_notes,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/incidents/<incident_id>/status", methods=["PUT"])
def update_incident_status(incident_id):
    """Update incident status"""
    data = request.json
    new_status = data.get("status")
    notes = data.get("notes", "")

    try:
        status = IncidentStatus(new_status)
    except ValueError:
        return jsonify({"success": False, "error": "Invalid status"}), 400

    incident = soc_simulator.update_incident_status(incident_id, status, notes)

    if not incident:
        return jsonify({"success": False, "error": "Incident not found"}), 404

    return jsonify({
        "success": True,
        "incident": _serialize_incident(incident),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/incidents/<incident_id>/remediation", methods=["POST"])
def add_remediation_action(incident_id):
    """Add remediation action to incident"""
    data = request.json
    action = data.get("action")

    if not action:
        return jsonify({"success": False, "error": "Action required"}), 400

    incident = soc_simulator.add_remediation_action(incident_id, action)

    if not incident:
        return jsonify({"success": False, "error": "Incident not found"}), 404

    return jsonify({
        "success": True,
        "incident": _serialize_incident(incident),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/attack-simulation", methods=["GET"])
def get_attack_simulation():
    """Get attack simulation data"""
    attack_type = request.args.get("type", default="sql_injection", type=str)

    summary = attack_generator.get_attack_summary(attack_type)

    return jsonify({
        "success": True,
        "simulation": summary,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/attack-logs", methods=["GET"])
def get_attack_logs():
    """Get simulated attack logs"""
    attack_type = request.args.get("type", default="sql_injection", type=str)
    count = request.args.get("count", default=50, type=int)

    logs = attack_generator.generate_simulated_logs(attack_type, count)

    return jsonify({
        "success": True,
        "attack_type": attack_type,
        "logs": logs,
        "count": len(logs),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/threat-intelligence", methods=["GET"])
def get_threat_intelligence():
    """Get threat intelligence summary"""
    intel = threat_engine.generate_threat_report()

    return jsonify({
        "success": True,
        "intelligence": intel,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/threat-actor", methods=["POST"])
def analyze_threat_actor():
    """Analyze potential threat actor based on indicators"""
    data = request.json
    indicators = data.get("indicators", {})

    analysis = threat_engine.analyze_threat_actor(indicators)

    return jsonify({
        "success": True,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/threat-prediction", methods=["GET"])
def get_threat_prediction():
    """Get AI threat prediction for next likely attack"""
    threat = threat_engine.threat_database[random.randint(0, len(threat_engine.threat_database) - 1)]
    prediction = threat_engine.predict_next_attack(threat)

    return jsonify({
        "success": True,
        "threat": threat["name"],
        "prediction": prediction,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/anomalies", methods=["POST"])
def detect_anomalies():
    """Detect anomalies in event stream"""
    data = request.json
    events = data.get("events", [])

    anomalies = threat_engine.detect_anomalies(events)

    return jsonify({
        "success": True,
        "anomalies": anomalies,
        "count": len(anomalies),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/security-events", methods=["GET"])
def get_security_events():
    """Get recent security events"""
    limit = request.args.get("limit", default=100, type=int)

    events = soc_simulator.events[-limit:]

    return jsonify({
        "success": True,
        "events": [_serialize_event(e) for e in events],
        "count": len(events),
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/threat-heatmap", methods=["GET"])
def get_threat_heatmap():
    """Get threat heatmap visualization data"""
    heatmap = soc_simulator.get_threat_heatmap()

    return jsonify({
        "success": True,
        "heatmap": heatmap,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/mitre-coverage", methods=["GET"])
def get_mitre_coverage():
    """Get MITRE ATT&CK coverage"""
    coverage = soc_simulator._calculate_mitre_coverage()

    return jsonify({
        "success": True,
        "coverage": coverage,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/siem-metrics", methods=["GET"])
def get_siem_metrics():
    """Get SIEM-style metrics"""
    metrics = {
        "events_processed_today": random.randint(50000, 500000),
        "alerts_generated_today": random.randint(50, 500),
        "incidents_created_today": random.randint(5, 50),
        "mean_time_to_detect_minutes": random.randint(5, 60),
        "mean_time_to_respond_minutes": random.randint(10, 120),
        "mean_time_to_resolve_hours": random.randint(1, 48),
        "alert_accuracy_percentage": random.uniform(70, 95),
        "sla_compliance_percentage": random.uniform(85, 99),
        "analyst_workload": random.randint(10, 100),
    }

    return jsonify({
        "success": True,
        "metrics": metrics,
        "timestamp": datetime.now().isoformat(),
    })


@soc_api.route("/live-feed", methods=["GET"])
def get_live_feed():
    """Get live security event feed (WebSocket alternative)"""
    feed = {
        "new_events": random.randint(5, 20),
        "new_alerts": random.randint(0, 5),
        "new_incidents": random.randint(0, 2),
        "recent_activity": [
            {
                "type": random.choice(
                    ["Alert", "Incident", "Event", "Detection", "Remediation"]
                ),
                "severity": random.choice(["CRITICAL", "HIGH", "MEDIUM", "LOW"]),
                "message": random.choice([
                    "SQL Injection detected on API endpoint",
                    "Brute force attack blocked",
                    "Unauthorized access attempt",
                    "Malware signature matched",
                    "Data exfiltration prevented",
                ]),
                "timestamp": datetime.now().isoformat(),
            }
            for _ in range(random.randint(3, 8))
        ],
    }

    return jsonify({
        "success": True,
        "feed": feed,
        "timestamp": datetime.now().isoformat(),
    })


# Helper functions
def _get_risk_level(threat_score: float) -> str:
    """Determine risk level from threat score"""
    if threat_score >= 80:
        return "CRITICAL"
    elif threat_score >= 60:
        return "HIGH"
    elif threat_score >= 40:
        return "MEDIUM"
    elif threat_score >= 20:
        return "LOW"
    else:
        return "MINIMAL"


def _serialize_alert(alert):
    """Serialize alert object"""
    return {
        "alert_id": alert.alert_id,
        "timestamp": alert.timestamp.isoformat(),
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity.name,
        "attack_type": alert.attack_type.name,
        "mitre_attack_id": alert.mitre_attack_id,
        "event_count": alert.event_count,
        "source_ips": alert.source_ips,
        "target_systems": alert.target_systems,
        "affected_users": alert.affected_users,
        "confidence_score": alert.confidence_score,
        "status": alert.status,
    }


def _serialize_incident(incident):
    """Serialize incident object"""
    return {
        "incident_id": incident.incident_id,
        "created_at": incident.created_at.isoformat(),
        "severity": incident.severity.name,
        "title": incident.title,
        "description": incident.description,
        "attack_type": incident.attack_type.name,
        "mitre_tactic": incident.mitre_tactic,
        "status": incident.status.value,
        "alert_count": len(incident.alerts),
        "affected_systems": incident.affected_systems,
        "affected_users": incident.affected_users,
        "root_cause": incident.root_cause,
        "remediation_actions": incident.remediation_actions,
        "assigned_analyst": incident.assigned_analyst,
        "sla_breach": incident.sla_breach,
        "impact_assessment": incident.impact_assessment,
    }


def _serialize_event(event):
    """Serialize event object"""
    return {
        "event_id": event.event_id,
        "timestamp": event.timestamp.isoformat(),
        "source_ip": event.source_ip,
        "target": event.target,
        "event_type": event.event_type,
        "severity": event.severity.name,
        "description": event.description,
        "mitre_attack_id": event.mitre_attack_id,
        "affected_asset": event.affected_asset,
    }
