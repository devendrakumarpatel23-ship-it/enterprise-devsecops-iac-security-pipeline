"""
AI-Powered Risk Scoring Engine
Calculates risk scores from CVSS, exploitability, exposure, and asset sensitivity
"""
import json
import math
from datetime import datetime
from typing import Dict, List, Tuple
from enum import Enum


class ExploitabilityLevel(Enum):
    """Exploitability classification levels"""
    UNPROVEN = 0.85
    PROOF_OF_CONCEPT = 0.90
    FUNCTIONAL = 0.95
    HIGH = 1.00


class ExposureLevel(Enum):
    """Asset exposure classification"""
    INTERNAL_ONLY = 0.22
    LOCAL_NETWORK = 0.56
    ADJACENT_NETWORK = 0.68
    PUBLIC = 1.00


class AssetSensitivity(Enum):
    """Asset data sensitivity classification"""
    LOW = 0.5
    MEDIUM = 0.75
    HIGH = 0.90
    CRITICAL = 1.00


class MITREATTACKPhase(Enum):
    """MITRE ATT&CK framework phases"""
    RECONNAISSANCE = "Initial Access"
    INITIAL_ACCESS = "Execution"
    EXECUTION = "Persistence"
    PERSISTENCE = "Privilege Escalation"
    PRIVILEGE_ESCALATION = "Credential Access"
    CREDENTIAL_ACCESS = "Discovery"
    DISCOVERY = "Lateral Movement"
    LATERAL_MOVEMENT = "Collection"
    COLLECTION = "Defense Evasion"
    COMMAND_AND_CONTROL = "Command and Control"
    EXFILTRATION = "Exfiltration"
    IMPACT = "Impact"


class Vulnerability:
    """Represents a detected vulnerability"""

    def __init__(
        self,
        cve_id: str,
        cvss_score: float,
        exploitability: ExploitabilityLevel,
        exposure: ExposureLevel,
        asset_sensitivity: AssetSensitivity,
        description: str,
        affected_systems: List[str],
        mitre_techniques: List[str] = None,
    ):
        self.cve_id = cve_id
        self.cvss_score = cvss_score
        self.exploitability = exploitability
        self.exposure = exposure
        self.asset_sensitivity = asset_sensitivity
        self.description = description
        self.affected_systems = affected_systems
        self.mitre_techniques = mitre_techniques or []
        self.discovered_date = datetime.now().isoformat()
        self.risk_score = self._calculate_risk_score()
        self.priority_level = self._determine_priority()

    def _calculate_risk_score(self) -> float:
        """
        Calculate risk score using formula:
        Risk Score = (CVSS × Exploitability × Exposure × Asset Sensitivity) × 100
        """
        risk = (
            self.cvss_score
            * self.exploitability.value
            * self.exposure.value
            * self.asset_sensitivity.value
        )
        # Normalize to 0-100 scale
        return min(100, round(risk * 100, 2))

    def _determine_priority(self) -> str:
        """Determine priority based on risk score"""
        if self.risk_score >= 80:
            return "CRITICAL"
        elif self.risk_score >= 60:
            return "HIGH"
        elif self.risk_score >= 40:
            return "MEDIUM"
        elif self.risk_score >= 20:
            return "LOW"
        else:
            return "INFORMATIONAL"

    def predict_attack_likelihood(self) -> Dict:
        """Predict likelihood of attack within next 30 days"""
        base_likelihood = self.risk_score / 100
        
        # Factors that increase likelihood
        is_public_exploit = "public" in self.description.lower()
        is_actively_exploited = "active" in self.description.lower()
        
        likelihood = base_likelihood
        if is_public_exploit:
            likelihood *= 1.3
        if is_actively_exploited:
            likelihood *= 1.5
        
        return {
            "vulnerability": self.cve_id,
            "attack_likelihood_30_days": round(min(1.0, likelihood), 3),
            "confidence": "high" if likelihood > 0.7 else "medium" if likelihood > 0.4 else "low",
            "factors": {
                "base_risk_score": self.risk_score,
                "public_exploit": is_public_exploit,
                "active_exploitation": is_actively_exploited,
            },
        }

    def to_dict(self) -> Dict:
        """Convert vulnerability to dictionary"""
        return {
            "cve_id": self.cve_id,
            "cvss_score": self.cvss_score,
            "risk_score": self.risk_score,
            "priority": self.priority_level,
            "exploitability": self.exploitability.name,
            "exposure": self.exposure.name,
            "asset_sensitivity": self.asset_sensitivity.name,
            "description": self.description,
            "affected_systems": self.affected_systems,
            "mitre_techniques": self.mitre_techniques,
            "discovered_date": self.discovered_date,
            "attack_prediction": self.predict_attack_likelihood(),
        }


class AIRiskEngine:
    """Main AI Risk Engine for enterprise security"""

    def __init__(self):
        self.vulnerabilities: List[Vulnerability] = []
        self.mitre_matrix = self._build_mitre_matrix()

    def _build_mitre_matrix(self) -> Dict:
        """Build MITRE ATT&CK matrix structure"""
        return {
            "tactics": {
                "reconnaissance": {
                    "techniques": [
                        "T1592 - Gather Victim Host Information",
                        "T1589 - Gather Victim Identity Information",
                    ]
                },
                "initial_access": {
                    "techniques": [
                        "T1566 - Phishing",
                        "T1190 - Exploit Public-Facing Application",
                    ]
                },
                "execution": {
                    "techniques": [
                        "T1203 - Exploitation for Client Execution",
                        "T1204 - User Execution",
                    ]
                },
                "persistence": {
                    "techniques": [
                        "T1547 - Boot or Logon Autostart Execution",
                        "T1137 - Office Application Startup",
                    ]
                },
                "privilege_escalation": {
                    "techniques": [
                        "T1134 - Access Token Manipulation",
                        "T1548 - Abuse Elevation Control Mechanism",
                    ]
                },
                "defense_evasion": {
                    "techniques": [
                        "T1548 - Abuse Elevation Control Mechanism",
                        "T1197 - BITS Jobs",
                    ]
                },
                "credential_access": {
                    "techniques": [
                        "T1110 - Brute Force",
                        "T1187 - Forced Authentication",
                    ]
                },
                "discovery": {
                    "techniques": [
                        "T1087 - Account Discovery",
                        "T1526 - Cloud Service Discovery",
                    ]
                },
                "lateral_movement": {
                    "techniques": [
                        "T1570 - Lateral Tool Transfer",
                        "T1021 - Remote Services",
                    ]
                },
                "collection": {
                    "techniques": [
                        "T1123 - Audio Capture",
                        "T1119 - Automated Exfiltration",
                    ]
                },
                "command_and_control": {
                    "techniques": [
                        "T1071 - Application Layer Protocol",
                        "T1092 - Communication Through Removable Media",
                    ]
                },
                "exfiltration": {
                    "techniques": [
                        "T1020 - Automated Exfiltration",
                        "T1030 - Data Transfer Size Limits",
                    ]
                },
                "impact": {
                    "techniques": [
                        "T1531 - Account Access Removal",
                        "T1561 - Disk Wipe",
                    ]
                },
            }
        }

    def register_vulnerability(self, vulnerability: Vulnerability) -> Dict:
        """Register a new vulnerability"""
        self.vulnerabilities.append(vulnerability)
        return {
            "status": "registered",
            "cve_id": vulnerability.cve_id,
            "risk_score": vulnerability.risk_score,
            "priority": vulnerability.priority_level,
        }

    def get_prioritized_vulnerabilities(self, limit: int = 10) -> List[Dict]:
        """Get vulnerabilities sorted by risk score"""
        sorted_vulns = sorted(
            self.vulnerabilities, key=lambda v: v.risk_score, reverse=True
        )
        return [v.to_dict() for v in sorted_vulns[:limit]]

    def get_vulnerabilities_by_priority(self, priority: str) -> List[Dict]:
        """Get vulnerabilities filtered by priority level"""
        filtered = [v for v in self.vulnerabilities if v.priority_level == priority]
        return [v.to_dict() for v in filtered]

    def calculate_organizational_risk(self) -> Dict:
        """Calculate overall organizational risk"""
        if not self.vulnerabilities:
            return {
                "organizational_risk_score": 0,
                "threat_level": "LOW",
                "summary": "No vulnerabilities detected",
            }

        critical_count = sum(
            1 for v in self.vulnerabilities if v.priority_level == "CRITICAL"
        )
        high_count = sum(
            1 for v in self.vulnerabilities if v.priority_level == "HIGH"
        )
        avg_risk = sum(v.risk_score for v in self.vulnerabilities) / len(
            self.vulnerabilities
        )

        # Calculate org risk (weighted by criticality)
        org_risk = (critical_count * 35 + high_count * 15 + avg_risk) / 100

        threat_level = (
            "CRITICAL"
            if org_risk > 75
            else "HIGH"
            if org_risk > 50
            else "MEDIUM"
            if org_risk > 25
            else "LOW"
        )

        return {
            "organizational_risk_score": round(min(100, org_risk), 2),
            "threat_level": threat_level,
            "critical_vulnerabilities": critical_count,
            "high_vulnerabilities": high_count,
            "average_vulnerability_risk": round(avg_risk, 2),
            "total_vulnerabilities": len(self.vulnerabilities),
        }

    def map_to_mitre_attack(self, vulnerability: Vulnerability) -> Dict:
        """Map vulnerability to MITRE ATT&CK framework"""
        mapping = {
            "cve_id": vulnerability.cve_id,
            "mapped_tactics": [],
            "mapped_techniques": [],
        }

        for technique in vulnerability.mitre_techniques:
            for tactic, data in self.mitre_matrix["tactics"].items():
                if any(t.startswith(technique) for t in data["techniques"]):
                    if tactic not in mapping["mapped_tactics"]:
                        mapping["mapped_tactics"].append(tactic)
                    mapping["mapped_techniques"].extend(
                        [t for t in data["techniques"] if t.startswith(technique)]
                    )

        return mapping

    def get_remediation_recommendations(self, max_recommendations: int = 5) -> List[Dict]:
        """Generate AI-powered remediation recommendations"""
        critical_vulns = self.get_vulnerabilities_by_priority("CRITICAL")[:max_recommendations]

        recommendations = []
        for vuln_dict in critical_vulns:
            vuln = next(v for v in self.vulnerabilities if v.cve_id == vuln_dict["cve_id"])
            
            recommendation = {
                "cve_id": vuln.cve_id,
                "recommendation": f"Immediate patching required for {vuln.cve_id}",
                "severity": vuln.priority_level,
                "estimated_fix_time_minutes": 30 if vuln.risk_score > 80 else 60,
                "affected_systems": vuln.affected_systems,
                "steps": [
                    "Backup current configuration",
                    f"Apply patch for {vuln.cve_id}",
                    "Test in staging environment",
                    "Deploy to production",
                    "Verify remediation",
                ],
                "automation_available": True,
                "risk_if_not_patched": "System compromise possible within 7-30 days",
            }
            recommendations.append(recommendation)

        return recommendations

    def export_risk_report(self, filepath: str) -> bool:
        """Export risk analysis report to JSON"""
        report = {
            "report_generated": datetime.now().isoformat(),
            "organizational_risk": self.calculate_organizational_risk(),
            "vulnerabilities": self.get_prioritized_vulnerabilities(limit=20),
            "mitre_mappings": [
                self.map_to_mitre_attack(v) for v in self.vulnerabilities[:10]
            ],
            "recommendations": self.get_remediation_recommendations(),
            "statistics": {
                "total_vulnerabilities": len(self.vulnerabilities),
                "average_risk_score": round(
                    sum(v.risk_score for v in self.vulnerabilities)
                    / len(self.vulnerabilities)
                    if self.vulnerabilities
                    else 0,
                    2,
                ),
            },
        }

        try:
            with open(filepath, "w") as f:
                json.dump(report, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False


# Initialize engine and sample vulnerabilities
def create_sample_vulnerabilities() -> List[Vulnerability]:
    """Create sample vulnerabilities for demonstration"""
    return [
        Vulnerability(
            cve_id="CVE-2024-1234",
            cvss_score=9.8,
            exploitability=ExploitabilityLevel.HIGH,
            exposure=ExposureLevel.PUBLIC,
            asset_sensitivity=AssetSensitivity.CRITICAL,
            description="Remote Code Execution in authentication module. Public exploits available.",
            affected_systems=["api-server-01", "api-server-02", "api-server-03"],
            mitre_techniques=["T1190", "T1203"],
        ),
        Vulnerability(
            cve_id="CVE-2024-5678",
            cvss_score=8.6,
            exploitability=ExploitabilityLevel.FUNCTIONAL,
            exposure=ExposureLevel.PUBLIC,
            asset_sensitivity=AssetSensitivity.HIGH,
            description="SQL Injection vulnerability in product search API",
            affected_systems=["web-app-01", "web-app-02"],
            mitre_techniques=["T1190"],
        ),
        Vulnerability(
            cve_id="CVE-2024-9012",
            cvss_score=7.5,
            exploitability=ExploitabilityLevel.PROOF_OF_CONCEPT,
            exposure=ExposureLevel.PUBLIC,
            asset_sensitivity=AssetSensitivity.HIGH,
            description="XSS vulnerability in user profile pages",
            affected_systems=["web-app-01", "web-app-02", "web-app-03"],
            mitre_techniques=["T1204"],
        ),
        Vulnerability(
            cve_id="CVE-2024-3456",
            cvss_score=6.5,
            exploitability=ExploitabilityLevel.UNPROVEN,
            exposure=ExposureLevel.ADJACENT_NETWORK,
            asset_sensitivity=AssetSensitivity.MEDIUM,
            description="Weak password policy enforcement",
            affected_systems=["auth-service-01"],
            mitre_techniques=["T1110"],
        ),
        Vulnerability(
            cve_id="CVE-2024-7890",
            cvss_score=8.1,
            exploitability=ExploitabilityLevel.FUNCTIONAL,
            exposure=ExposureLevel.ADJACENT_NETWORK,
            asset_sensitivity=AssetSensitivity.HIGH,
            description="Privilege escalation via kernel driver",
            affected_systems=["server-01", "server-02"],
            mitre_techniques=["T1548"],
        ),
    ]


if __name__ == "__main__":
    # Demo
    engine = AIRiskEngine()
    for vuln in create_sample_vulnerabilities():
        engine.register_vulnerability(vuln)

    print("Organizational Risk:", engine.calculate_organizational_risk())
    print("\nTop Vulnerabilities:")
    for v in engine.get_prioritized_vulnerabilities(3):
        print(f"  - {v['cve_id']}: Risk Score {v['risk_score']} ({v['priority']})")

    print("\nRecommendations:")
    for r in engine.get_remediation_recommendations(2):
        print(f"  - {r['cve_id']}: {r['recommendation']}")

    engine.export_risk_report("risk_report.json")
    print("\nRisk report exported to risk_report.json")
