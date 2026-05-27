"""
Risk Dashboard API Endpoints
Provides REST API for security risk data and metrics
"""
from flask import Blueprint, jsonify, request, send_file
from datetime import datetime, timedelta
import json
from app.security.ai_risk_engine import (
    AIRiskEngine,
    Vulnerability,
    ExploitabilityLevel,
    ExposureLevel,
    AssetSensitivity,
    create_sample_vulnerabilities,
)

risk_api = Blueprint("risk_api", __name__, url_prefix="/api/security")

# Initialize engine with sample data
engine = AIRiskEngine()
for vuln in create_sample_vulnerabilities():
    engine.register_vulnerability(vuln)


@risk_api.route("/overview", methods=["GET"])
def get_security_overview():
    """Get security overview dashboard data"""
    org_risk = engine.calculate_organizational_risk()
    top_vulns = engine.get_prioritized_vulnerabilities(limit=5)

    return jsonify(
        {
            "organizational_risk": org_risk,
            "top_vulnerabilities": top_vulns,
            "critical_count": sum(1 for v in engine.vulnerabilities if v.priority_level == "CRITICAL"),
            "high_count": sum(1 for v in engine.vulnerabilities if v.priority_level == "HIGH"),
            "total_count": len(engine.vulnerabilities),
        }
    )


@risk_api.route("/vulnerabilities", methods=["GET"])
def get_vulnerabilities():
    """Get vulnerabilities with optional filtering"""
    priority = request.args.get("priority", "").upper()
    limit = request.args.get("limit", 20, type=int)

    if priority:
        vulns = engine.get_vulnerabilities_by_priority(priority)
    else:
        vulns = engine.get_prioritized_vulnerabilities(limit=limit)

    return jsonify({"vulnerabilities": vulns, "count": len(vulns)})


@risk_api.route("/vulnerabilities/<cve_id>", methods=["GET"])
def get_vulnerability_details(cve_id):
    """Get detailed information about a specific vulnerability"""
    vuln = next((v for v in engine.vulnerabilities if v.cve_id == cve_id), None)

    if not vuln:
        return jsonify({"error": "Vulnerability not found"}), 404

    return jsonify(
        {
            "vulnerability": vuln.to_dict(),
            "mitre_mapping": engine.map_to_mitre_attack(vuln),
            "attack_prediction": vuln.predict_attack_likelihood(),
        }
    )


@risk_api.route("/risk-score", methods=["GET"])
def get_risk_score():
    """Get current organizational risk score"""
    return jsonify(engine.calculate_organizational_risk())


@risk_api.route("/recommendations", methods=["GET"])
def get_recommendations():
    """Get AI-generated remediation recommendations"""
    limit = request.args.get("limit", 5, type=int)
    recommendations = engine.get_remediation_recommendations(max_recommendations=limit)

    return jsonify({"recommendations": recommendations, "count": len(recommendations)})


@risk_api.route("/trends", methods=["GET"])
def get_risk_trends():
    """Get risk trends over time"""
    days = request.args.get("days", 7, type=int)

    trend_data = []
    base_risk = engine.calculate_organizational_risk()["organizational_risk_score"]

    for i in range(days, 0, -1):
        variation = (i % 3) * 2 - 2
        trend_data.append(
            {
                "date": (datetime.now() - timedelta(days=i)).isoformat(),
                "risk_score": max(0, min(100, base_risk + variation)),
            }
        )

    return jsonify({"trends": trend_data})


@risk_api.route("/mitre-matrix", methods=["GET"])
def get_mitre_matrix():
    """Get MITRE ATT&CK matrix with detected techniques"""
    matrix_data = engine.mitre_matrix.copy()

    # Add detection info
    for tactic in matrix_data["tactics"]:
        detected_count = sum(
            1
            for v in engine.vulnerabilities
            if any(t in v.mitre_techniques for t in matrix_data["tactics"][tactic]["techniques"])
        )
        matrix_data["tactics"][tactic]["detected"] = detected_count

    return jsonify(matrix_data)


@risk_api.route("/compliance-status", methods=["GET"])
def get_compliance_status():
    """Get compliance framework status"""
    frameworks = {
        "PCI-DSS": {
            "score": 85,
            "controls": 12,
            "passing": 10,
            "failing": 2,
            "status": "warning",
        },
        "OWASP Top 10": {
            "score": 92,
            "controls": 10,
            "passing": 9,
            "failing": 1,
            "status": "good",
        },
        "CIS Benchmarks": {
            "score": 88,
            "controls": 20,
            "passing": 17,
            "failing": 3,
            "status": "warning",
        },
        "NIST Cybersecurity Framework": {
            "score": 79,
            "controls": 5,
            "passing": 4,
            "failing": 1,
            "status": "warning",
        },
        "SOC 2": {
            "score": 91,
            "controls": 15,
            "passing": 14,
            "failing": 1,
            "status": "good",
        },
        "ISO 27001": {
            "score": 84,
            "controls": 18,
            "passing": 15,
            "failing": 3,
            "status": "warning",
        },
    }

    return jsonify({"frameworks": frameworks})


@risk_api.route("/kpi-metrics", methods=["GET"])
def get_kpi_metrics():
    """Get security KPI metrics"""
    org_risk = engine.calculate_organizational_risk()

    kpis = {
        "security_score": {
            "value": round(100 - org_risk["organizational_risk_score"], 1),
            "trend": -2.5,
            "status": "warning",
        },
        "critical_cves": {
            "value": org_risk["critical_vulnerabilities"],
            "trend": 3.2,
            "status": "critical" if org_risk["critical_vulnerabilities"] > 5 else "warning",
        },
        "open_incidents": {"value": 47, "trend": 5.1, "status": "warning"},
        "compliant_assets": {"value": 94, "trend": 1.8, "status": "good"},
        "mean_time_to_detect": {"value": "2.3h", "trend": -15.2, "status": "good"},
        "mean_time_to_respond": {
            "value": "4.1h",
            "trend": -8.5,
            "status": "good",
        },
    }

    return jsonify(kpis)


@risk_api.route("/threat-events", methods=["GET"])
def get_threat_events():
    """Get simulated threat events"""
    events = [
        {
            "id": "EVT-001",
            "type": "unauthorized_access_attempt",
            "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "severity": "high",
            "description": "Multiple failed login attempts from 192.168.1.100",
            "affected_system": "auth-service-01",
        },
        {
            "id": "EVT-002",
            "type": "anomalous_api_traffic",
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "severity": "medium",
            "description": "Unusual API call pattern detected",
            "affected_system": "api-gateway",
        },
        {
            "id": "EVT-003",
            "type": "container_escape_attempt",
            "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "severity": "critical",
            "description": "Attempted container escape detected in web-app-02",
            "affected_system": "web-app-02",
        },
        {
            "id": "EVT-004",
            "type": "privilege_escalation",
            "timestamp": (datetime.now() - timedelta(minutes=45)).isoformat(),
            "severity": "critical",
            "description": "Unauthorized privilege escalation detected",
            "affected_system": "database-01",
        },
        {
            "id": "EVT-005",
            "type": "data_exfiltration",
            "timestamp": (datetime.now() - timedelta(minutes=60)).isoformat(),
            "severity": "high",
            "description": "Large data transfer detected to external IP",
            "affected_system": "api-server-01",
        },
    ]

    return jsonify({"events": events, "count": len(events)})


@risk_api.route("/report/download", methods=["GET"])
def download_report():
    """Generate and download security report"""
    report_format = request.args.get("format", "json").lower()

    report_data = {
        "report_generated": datetime.now().isoformat(),
        "organizational_risk": engine.calculate_organizational_risk(),
        "vulnerabilities": engine.get_prioritized_vulnerabilities(limit=20),
        "recommendations": engine.get_remediation_recommendations(),
        "kpis": json.loads(get_kpi_metrics().get_json()),
    }

    if report_format == "json":
        filename = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/tmp/{filename}"
        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=2)
        return send_file(filepath, as_attachment=True, download_name=filename)

    return jsonify({"error": "Unsupported format"}), 400


@risk_api.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "engine": "AIRiskEngine",
            "vulnerabilities_tracked": len(engine.vulnerabilities),
            "timestamp": datetime.now().isoformat(),
        }
    )


# Error handlers
@risk_api.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@risk_api.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
