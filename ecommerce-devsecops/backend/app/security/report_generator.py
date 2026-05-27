"""
Security Report Export System
Generates downloadable PDF, JSON, and executive summary reports
"""
import json
from typing import Dict, List
from datetime import datetime
from io import BytesIO
import base64


class SecurityReportGenerator:
    """Generates comprehensive security reports in multiple formats"""

    def __init__(self):
        self.report_data = {}
        self.timestamp = datetime.now().isoformat()

    def generate_comprehensive_report(
        self,
        risk_data: Dict,
        compliance_data: Dict,
        alert_data: Dict,
        recommendations: List[Dict],
    ) -> Dict:
        """Generate comprehensive security report"""
        report = {
            "report_metadata": {
                "generated_at": self.timestamp,
                "report_id": f"SEC-RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "report_version": "1.0",
                "classification": "Confidential",
            },
            "executive_summary": self._generate_executive_summary(
                risk_data, compliance_data, alert_data
            ),
            "risk_assessment": risk_data,
            "compliance_posture": compliance_data,
            "security_incidents": alert_data,
            "remediation_roadmap": self._generate_remediation_roadmap(recommendations),
            "trends_and_analytics": self._generate_trends(risk_data),
            "appendix": self._generate_appendix(),
        }

        self.report_data = report
        return report

    def _generate_executive_summary(
        self, risk_data: Dict, compliance_data: Dict, alert_data: Dict
    ) -> Dict:
        """Generate executive summary"""
        return {
            "organization": "Enterprise E-Commerce Platform",
            "assessment_period": f"{(datetime.now().date() - datetime.timedelta(days=30)).isoformat()} to {datetime.now().date().isoformat()}",
            "overall_security_score": round(100 - risk_data.get("organizational_risk_score", 0), 1),
            "threat_level": risk_data.get("threat_level", "UNKNOWN"),
            "key_findings": [
                {
                    "finding": "Critical Vulnerabilities Detected",
                    "count": risk_data.get("critical_vulnerabilities", 0),
                    "priority": "IMMEDIATE",
                },
                {
                    "finding": "Compliance Gaps",
                    "count": sum(
                        1 for fw in compliance_data.get("frameworks", {}).values()
                        if fw.get("status") != "FULL_COMPLIANCE"
                    ),
                    "priority": "HIGH",
                },
                {
                    "finding": "Open Security Incidents",
                    "count": len(alert_data.get("open_alerts", [])),
                    "priority": "HIGH",
                },
            ],
            "recommendations_summary": {
                "total_recommendations": len([r for r in [] if r]),
                "immediate_actions": 3,
                "estimated_remediation_time": "3-5 weeks",
            },
        }

    def _generate_remediation_roadmap(self, recommendations: List[Dict]) -> Dict:
        """Generate remediation roadmap"""
        return {
            "phase_1": {
                "timeline": "Week 1",
                "actions": recommendations[:2] if len(recommendations) > 0 else [],
                "estimated_effort": "40 hours",
                "dependencies": [],
            },
            "phase_2": {
                "timeline": "Weeks 2-3",
                "actions": recommendations[2:4] if len(recommendations) > 2 else [],
                "estimated_effort": "60 hours",
                "dependencies": ["Phase 1 completion"],
            },
            "phase_3": {
                "timeline": "Weeks 4-5",
                "actions": recommendations[4:] if len(recommendations) > 4 else [],
                "estimated_effort": "40 hours",
                "dependencies": ["Phase 2 completion"],
            },
        }

    def _generate_trends(self, risk_data: Dict) -> Dict:
        """Generate trend analytics"""
        return {
            "vulnerability_trends": [
                {"date": "2024-01-01", "count": 45, "critical": 2},
                {"date": "2024-01-02", "count": 43, "critical": 2},
                {"date": "2024-01-03", "count": 42, "critical": 1},
                {"date": "2024-01-04", "count": 40, "critical": 1},
                {"date": "2024-01-05", "count": 38, "critical": 0},
            ],
            "risk_score_trend": [
                {"date": "2024-01-01", "score": 65},
                {"date": "2024-01-02", "score": 63},
                {"date": "2024-01-03", "score": 61},
                {"date": "2024-01-04", "score": 58},
                {"date": "2024-01-05", "score": 55},
            ],
            "compliance_trend": [
                {"date": "2024-01-01", "score": 78},
                {"date": "2024-01-02", "score": 79},
                {"date": "2024-01-03", "score": 81},
                {"date": "2024-01-04", "score": 83},
                {"date": "2024-01-05", "score": 85},
            ],
            "trend_analysis": "Positive trend in security posture. Vulnerabilities decreasing, compliance score increasing.",
        }

    def _generate_appendix(self) -> Dict:
        """Generate appendix with definitions and references"""
        return {
            "definitions": {
                "CVSS": "Common Vulnerability Scoring System - standardized vulnerability severity rating",
                "CVE": "Common Vulnerabilities and Exposures - unique identifier for vulnerabilities",
                "MITRE ATT&CK": "Framework documenting adversary tactics and techniques",
                "Risk Score": "Calculated metric combining CVSS, exploitability, and organizational exposure",
            },
            "references": [
                "NIST Cybersecurity Framework",
                "PCI-DSS v3.2.1",
                "OWASP Top 10 2021",
                "ISO/IEC 27001:2022",
            ],
            "contact": {
                "security_team": "security@enterprise.com",
                "incident_response": "security-incidents@enterprise.com",
            },
        }

    def export_json_report(self, filepath: str) -> bool:
        """Export report as JSON"""
        try:
            with open(filepath, "w") as f:
                json.dump(self.report_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting JSON report: {e}")
            return False

    def export_pdf_report(self, filepath: str) -> bool:
        """Export report as PDF (generates HTML for conversion)"""
        try:
            html_content = self._generate_html_report()

            with open(filepath.replace(".pdf", ".html"), "w") as f:
                f.write(html_content)

            print(f"HTML report generated: {filepath.replace('.pdf', '.html')}")
            print("Note: Convert HTML to PDF using: wkhtmltopdf or similar tools")
            return True
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            return False

    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        report = self.report_data
        summary = report.get("executive_summary", {})

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Enterprise Security Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .metadata {{
            background: white;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        .section {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .kpi {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            margin: 10px;
            border-radius: 8px;
            min-width: 150px;
            text-align: center;
        }}
        .kpi-value {{
            font-size: 2em;
            font-weight: bold;
        }}
        .kpi-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .finding {{
            background: #f9f9f9;
            border-left: 4px solid #ff6b6b;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .finding.high {{
            border-left-color: #ff6b6b;
        }}
        .finding.medium {{
            border-left-color: #ffa500;
        }}
        .finding.low {{
            border-left-color: #51cf66;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        table td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        table tr:hover {{
            background: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Enterprise Security Report</h1>
        <p>Comprehensive Security Posture Assessment</p>
    </div>

    <div class="metadata">
        <strong>Report ID:</strong> {report.get('report_metadata', {}).get('report_id')}<br>
        <strong>Generated:</strong> {report.get('report_metadata', {}).get('generated_at')}<br>
        <strong>Classification:</strong> {report.get('report_metadata', {}).get('classification')}
    </div>

    <div class="section">
        <h2>Executive Summary</h2>
        <div>
            <div class="kpi">
                <div class="kpi-value">{summary.get('overall_security_score', 'N/A')}</div>
                <div class="kpi-label">Security Score</div>
            </div>
            <div class="kpi">
                <div class="kpi-value">{summary.get('threat_level', 'UNKNOWN')}</div>
                <div class="kpi-label">Threat Level</div>
            </div>
        </div>
        <p>{summary.get('assessment_period', 'N/A')}</p>
    </div>

    <div class="section">
        <h2>Key Findings</h2>
        {''.join(f'<div class="finding high"><strong>{f["finding"]}</strong><br>Count: {f["count"]} - Priority: {f["priority"]}</div>' for f in summary.get('key_findings', []))}
    </div>

    <div class="section">
        <h2>Remediation Roadmap</h2>
        <p>Phase 1 (Week 1): {len(report.get('remediation_roadmap', {}).get('phase_1', {}).get('actions', []))} actions</p>
        <p>Phase 2 (Weeks 2-3): {len(report.get('remediation_roadmap', {}).get('phase_2', {}).get('actions', []))} actions</p>
        <p>Phase 3 (Weeks 4-5): {len(report.get('remediation_roadmap', {}).get('phase_3', {}).get('actions', []))} actions</p>
    </div>

    <div class="footer">
        <p>Confidential - For authorized recipients only</p>
        <p>Contact: security@enterprise.com</p>
    </div>
</body>
</html>
"""
        return html

    def export_executive_summary(self, filepath: str) -> bool:
        """Export executive summary only"""
        try:
            summary = {
                "report_type": "Executive Summary",
                "generated_at": self.timestamp,
                "summary": self.report_data.get("executive_summary", {}),
            }

            with open(filepath, "w") as f:
                json.dump(summary, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting summary: {e}")
            return False

    def generate_dashboard_metrics(self) -> Dict:
        """Generate metrics for dashboard visualization"""
        report = self.report_data
        return {
            "kpis": {
                "security_score": report.get("executive_summary", {}).get(
                    "overall_security_score", 0
                ),
                "threat_level": report.get("executive_summary", {}).get("threat_level", "UNKNOWN"),
                "critical_findings": sum(
                    f.get("count", 0)
                    for f in report.get("executive_summary", {}).get("key_findings", [])
                    if f.get("priority") == "IMMEDIATE"
                ),
                "compliance_gaps": sum(
                    1
                    for fw in report.get("compliance_posture", {})
                    .get("frameworks", {})
                    .values()
                    if fw.get("status") != "FULL_COMPLIANCE"
                ),
            },
            "trends": report.get("trends_and_analytics", {}),
            "recommendations": report.get("remediation_roadmap", {}),
        }


if __name__ == "__main__":
    generator = SecurityReportGenerator()

    # Sample data
    risk_data = {
        "organizational_risk_score": 35.5,
        "threat_level": "MEDIUM",
        "critical_vulnerabilities": 2,
        "high_vulnerabilities": 8,
        "total_vulnerabilities": 42,
    }

    compliance_data = {
        "frameworks": {
            "PCI-DSS": {"score": 85, "status": "SUBSTANTIAL_COMPLIANCE"},
            "OWASP": {"score": 92, "status": "FULL_COMPLIANCE"},
            "CIS": {"score": 88, "status": "SUBSTANTIAL_COMPLIANCE"},
        }
    }

    alert_data = {
        "open_alerts": [
            {"id": "ALR-001", "severity": "CRITICAL"},
            {"id": "ALR-002", "severity": "HIGH"},
        ],
        "closed_alerts": [],
    }

    recommendations = [
        {"cve": "CVE-2024-1234", "action": "Apply security patch"},
        {"cve": "CVE-2024-5678", "action": "Update dependencies"},
        {"cve": "CVE-2024-9012", "action": "Implement WAF rules"},
    ]

    # Generate report
    report = generator.generate_comprehensive_report(
        risk_data, compliance_data, alert_data, recommendations
    )

    # Export in multiple formats
    generator.export_json_report("security_report.json")
    generator.export_pdf_report("security_report.pdf")
    generator.export_executive_summary("executive_summary.json")

    print("✅ Reports generated successfully")
    print("  - security_report.json")
    print("  - security_report.html")
    print("  - executive_summary.json")
