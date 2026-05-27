"""
MITRE ATT&CK Framework Mapping Engine
Maps vulnerabilities and attack patterns to MITRE ATT&CK tactics and techniques
"""
import json
from typing import Dict, List, Set
from datetime import datetime


class MITREATTACKEngine:
    """Engine for MITRE ATT&CK framework mapping and analysis"""

    def __init__(self):
        self.matrix = self._initialize_matrix()
        self.detections = {}
        self.threat_intelligence = self._load_threat_intel()

    def _initialize_matrix(self) -> Dict:
        """Initialize comprehensive MITRE ATT&CK matrix"""
        return {
            "reconnaissance": {
                "id": "TA0043",
                "techniques": {
                    "T1592": {
                        "name": "Gather Victim Host Information",
                        "subtechniques": ["T1592.001", "T1592.002", "T1592.003"],
                    },
                    "T1589": {
                        "name": "Gather Victim Identity Information",
                        "subtechniques": ["T1589.001", "T1589.002"],
                    },
                    "T1590": {
                        "name": "Gather Victim Network Information",
                        "subtechniques": ["T1590.001", "T1590.002"],
                    },
                },
            },
            "resource_development": {
                "id": "TA0042",
                "techniques": {
                    "T1583": {
                        "name": "Acquire Infrastructure",
                        "subtechniques": ["T1583.001", "T1583.002"],
                    },
                    "T1586": {
                        "name": "Compromise Accounts",
                        "subtechniques": ["T1586.001", "T1586.002"],
                    },
                },
            },
            "initial_access": {
                "id": "TA0001",
                "techniques": {
                    "T1189": {
                        "name": "Drive-by Compromise",
                        "subtechniques": [],
                    },
                    "T1200": {
                        "name": "Hardware Additions",
                        "subtechniques": [],
                    },
                    "T1566": {
                        "name": "Phishing",
                        "subtechniques": ["T1566.001", "T1566.002", "T1566.003"],
                    },
                    "T1091": {
                        "name": "Replication Through Removable Media",
                        "subtechniques": [],
                    },
                    "T1199": {
                        "name": "Trusted Relationship",
                        "subtechniques": [],
                    },
                    "T1199": {
                        "name": "Exploit Public-Facing Application",
                        "subtechniques": [],
                    },
                },
            },
            "execution": {
                "id": "TA0002",
                "techniques": {
                    "T1059": {
                        "name": "Command and Scripting Interpreter",
                        "subtechniques": ["T1059.001", "T1059.002", "T1059.003"],
                    },
                    "T1203": {
                        "name": "Exploitation for Client Execution",
                        "subtechniques": [],
                    },
                    "T1559": {
                        "name": "Inter-Process Communication",
                        "subtechniques": ["T1559.001", "T1559.002"],
                    },
                    "T1106": {
                        "name": "Native API",
                        "subtechniques": [],
                    },
                },
            },
            "persistence": {
                "id": "TA0003",
                "techniques": {
                    "T1098": {
                        "name": "Account Manipulation",
                        "subtechniques": ["T1098.001", "T1098.002"],
                    },
                    "T1197": {
                        "name": "BITS Jobs",
                        "subtechniques": [],
                    },
                    "T1547": {
                        "name": "Boot or Logon Autostart Execution",
                        "subtechniques": ["T1547.001", "T1547.004"],
                    },
                    "T1547": {
                        "name": "Browser Extensions",
                        "subtechniques": [],
                    },
                },
            },
            "privilege_escalation": {
                "id": "TA0004",
                "techniques": {
                    "T1134": {
                        "name": "Access Token Manipulation",
                        "subtechniques": ["T1134.001", "T1134.002"],
                    },
                    "T1548": {
                        "name": "Abuse Elevation Control Mechanism",
                        "subtechniques": ["T1548.002", "T1548.003"],
                    },
                    "T1547": {
                        "name": "Boot or Logon Autostart Execution",
                        "subtechniques": ["T1547.001"],
                    },
                    "T1037": {
                        "name": "Boot or Logon Initialization Scripts",
                        "subtechniques": ["T1037.001", "T1037.002"],
                    },
                },
            },
            "defense_evasion": {
                "id": "TA0005",
                "techniques": {
                    "T1197": {
                        "name": "BITS Jobs",
                        "subtechniques": [],
                    },
                    "T1197": {
                        "name": "Masquerading",
                        "subtechniques": ["T1556.001", "T1556.002"],
                    },
                    "T1218": {
                        "name": "System Binary Proxy Execution",
                        "subtechniques": ["T1218.001", "T1218.003"],
                    },
                    "T1221": {
                        "name": "Template Injection",
                        "subtechniques": [],
                    },
                },
            },
            "credential_access": {
                "id": "TA0006",
                "techniques": {
                    "T1110": {
                        "name": "Brute Force",
                        "subtechniques": ["T1110.001", "T1110.002"],
                    },
                    "T1187": {
                        "name": "Forced Authentication",
                        "subtechniques": [],
                    },
                    "T1056": {
                        "name": "Input Capture",
                        "subtechniques": ["T1056.001", "T1056.002"],
                    },
                    "T1040": {
                        "name": "Network Sniffing",
                        "subtechniques": [],
                    },
                },
            },
            "discovery": {
                "id": "TA0007",
                "techniques": {
                    "T1087": {
                        "name": "Account Discovery",
                        "subtechniques": ["T1087.001", "T1087.002"],
                    },
                    "T1010": {
                        "name": "Application Window Discovery",
                        "subtechniques": [],
                    },
                    "T1217": {
                        "name": "Browser Bookmark Discovery",
                        "subtechniques": [],
                    },
                    "T1580": {
                        "name": "Cloud Infrastructure Discovery",
                        "subtechniques": [],
                    },
                },
            },
            "lateral_movement": {
                "id": "TA0008",
                "techniques": {
                    "T1210": {
                        "name": "Exploitation of Remote Services",
                        "subtechniques": [],
                    },
                    "T1570": {
                        "name": "Lateral Tool Transfer",
                        "subtechniques": [],
                    },
                    "T1021": {
                        "name": "Remote Services",
                        "subtechniques": ["T1021.001", "T1021.002", "T1021.006"],
                    },
                },
            },
            "collection": {
                "id": "TA0009",
                "techniques": {
                    "T1123": {
                        "name": "Audio Capture",
                        "subtechniques": [],
                    },
                    "T1119": {
                        "name": "Automated Exfiltration",
                        "subtechniques": [],
                    },
                    "T1115": {
                        "name": "Clipboard Data",
                        "subtechniques": [],
                    },
                    "T1530": {
                        "name": "Data from Cloud Storage Object",
                        "subtechniques": [],
                    },
                },
            },
            "command_and_control": {
                "id": "TA0011",
                "techniques": {
                    "T1071": {
                        "name": "Application Layer Protocol",
                        "subtechniques": ["T1071.001", "T1071.002"],
                    },
                    "T1092": {
                        "name": "Communication Through Removable Media",
                        "subtechniques": [],
                    },
                    "T1008": {
                        "name": "Fallback Channels",
                        "subtechniques": [],
                    },
                    "T1573": {
                        "name": "Encrypted Channel",
                        "subtechniques": ["T1573.001", "T1573.002"],
                    },
                },
            },
            "exfiltration": {
                "id": "TA0010",
                "techniques": {
                    "T1020": {
                        "name": "Automated Exfiltration",
                        "subtechniques": [],
                    },
                    "T1030": {
                        "name": "Data Transfer Size Limits",
                        "subtechniques": [],
                    },
                    "T1048": {
                        "name": "Exfiltration Over Alternative Protocol",
                        "subtechniques": ["T1048.001", "T1048.002"],
                    },
                    "T1041": {
                        "name": "Exfiltration Over C2 Channel",
                        "subtechniques": [],
                    },
                },
            },
            "impact": {
                "id": "TA0040",
                "techniques": {
                    "T1531": {
                        "name": "Account Access Removal",
                        "subtechniques": [],
                    },
                    "T1531": {
                        "name": "Data Destruction",
                        "subtechniques": ["T1561.001", "T1561.002"],
                    },
                    "T1561": {
                        "name": "Disk Wipe",
                        "subtechniques": ["T1561.001", "T1561.002"],
                    },
                    "T1499": {
                        "name": "Endpoint Denial of Service",
                        "subtechniques": ["T1499.001", "T1499.002"],
                    },
                },
            },
        }

    def _load_threat_intel(self) -> Dict:
        """Load threat intelligence data"""
        return {
            "T1566": {
                "name": "Phishing",
                "known_campaigns": ["Campaign A", "Campaign B"],
                "associated_malware": ["Emotet", "Trickbot"],
                "prevalence": "high",
            },
            "T1190": {
                "name": "Exploit Public-Facing Application",
                "known_campaigns": ["Campaign C"],
                "associated_malware": ["CVE-2024-1234 Exploiter"],
                "prevalence": "critical",
            },
            "T1110": {
                "name": "Brute Force",
                "known_campaigns": ["Campaign D"],
                "associated_malware": [],
                "prevalence": "medium",
            },
        }

    def map_vulnerability_to_techniques(
        self, vuln_description: str, cve_id: str
    ) -> List[str]:
        """Map vulnerability to MITRE ATT&CK techniques based on description"""
        mapped_techniques = []

        # Keyword-based mapping
        keywords = {
            "rce|remote code": ["T1059", "T1203"],
            "sql injection": ["T1190"],
            "xss|cross-site": ["T1204"],
            "privilege escalation": ["T1548", "T1134"],
            "authentication|brute force": ["T1110"],
            "data exfiltration": ["T1020", "T1041"],
            "credential": ["T1110", "T1187"],
            "ransomware": ["T1561"],
            "malware": ["T1203", "T1566"],
        }

        desc_lower = vuln_description.lower()
        for keyword_pattern, techniques in keywords.items():
            if any(kw in desc_lower for kw in keyword_pattern.split("|")):
                mapped_techniques.extend(techniques)

        return list(set(mapped_techniques))

    def analyze_attack_chain(self, techniques: List[str]) -> Dict:
        """Analyze potential attack chain from techniques"""
        chain = {
            "attack_phases": [],
            "potential_flow": [],
            "risk_level": "UNKNOWN",
        }

        phase_order = [
            "reconnaissance",
            "resource_development",
            "initial_access",
            "execution",
            "persistence",
            "privilege_escalation",
            "defense_evasion",
            "credential_access",
            "discovery",
            "lateral_movement",
            "collection",
            "command_and_control",
            "exfiltration",
            "impact",
        ]

        matched_phases = set()
        for phase in phase_order:
            phase_techniques = self.matrix[phase]["techniques"]
            for tech_id in techniques:
                if tech_id in phase_techniques:
                    matched_phases.add(phase)

        chain["attack_phases"] = sorted(
            matched_phases, key=lambda x: phase_order.index(x)
        )
        chain["potential_flow"] = " -> ".join(chain["attack_phases"])

        if len(matched_phases) > 8:
            chain["risk_level"] = "CRITICAL"
        elif len(matched_phases) > 5:
            chain["risk_level"] = "HIGH"
        elif len(matched_phases) > 2:
            chain["risk_level"] = "MEDIUM"
        else:
            chain["risk_level"] = "LOW"

        return chain

    def get_technique_details(self, technique_id: str) -> Dict:
        """Get detailed information about a technique"""
        for tactic, tactic_data in self.matrix.items():
            if technique_id in tactic_data["techniques"]:
                technique = tactic_data["techniques"][technique_id]
                threat_info = self.threat_intelligence.get(
                    technique_id,
                    {"campaigns": [], "associated_malware": [], "prevalence": "unknown"},
                )

                return {
                    "technique_id": technique_id,
                    "tactic": tactic,
                    "name": technique["name"],
                    "subtechniques": technique.get("subtechniques", []),
                    "threat_intelligence": threat_info,
                }

        return {"error": "Technique not found"}

    def build_heatmap_data(self) -> Dict:
        """Build heatmap data for matrix visualization"""
        heatmap = {}
        for tactic, tactic_data in self.matrix.items():
            heatmap[tactic] = {}
            for tech_id, technique in tactic_data["techniques"].items():
                heatmap[tactic][tech_id] = {
                    "name": technique["name"],
                    "detected": False,
                    "severity": "low",
                }

        return heatmap

    def export_matrix_json(self, filepath: str) -> bool:
        """Export matrix to JSON"""
        try:
            with open(filepath, "w") as f:
                json.dump(self.matrix, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting matrix: {e}")
            return False

    def generate_attack_report(self, detected_techniques: List[str]) -> Dict:
        """Generate comprehensive attack analysis report"""
        report = {
            "report_generated": datetime.now().isoformat(),
            "detected_techniques": detected_techniques,
            "attack_chain_analysis": self.analyze_attack_chain(detected_techniques),
            "detailed_techniques": [
                self.get_technique_details(t) for t in detected_techniques
            ],
            "recommendations": self._generate_mitigations(detected_techniques),
        }

        return report

    def _generate_mitigations(self, techniques: List[str]) -> List[Dict]:
        """Generate mitigation recommendations"""
        mitigations = []

        phase_mitigations = {
            "initial_access": [
                "Implement email filtering and anti-phishing measures",
                "Block known malicious domains and IPs",
            ],
            "execution": [
                "Disable unnecessary scripting interpreters",
                "Enforce code execution policies",
            ],
            "persistence": [
                "Monitor startup locations and scheduled tasks",
                "Implement integrity monitoring",
            ],
            "privilege_escalation": [
                "Apply least privilege principles",
                "Keep systems patched and updated",
            ],
            "lateral_movement": [
                "Implement network segmentation",
                "Monitor lateral movement indicators",
            ],
            "exfiltration": ["Enable data loss prevention (DLP)", "Monitor outbound traffic"],
            "impact": ["Implement backup and recovery procedures", "Monitor for destructive actions"],
        }

        for tactic, recommendations in phase_mitigations.items():
            if any(
                t in self.matrix.get(tactic, {}).get("techniques", {})
                for t in techniques
            ):
                for rec in recommendations:
                    mitigations.append({"tactic": tactic, "recommendation": rec})

        return mitigations


if __name__ == "__main__":
    engine = MITREATTACKEngine()

    # Example vulnerability mapping
    vuln_desc = "Remote Code Execution vulnerability allows unauthenticated attackers to execute arbitrary code"
    techniques = engine.map_vulnerability_to_techniques(vuln_desc, "CVE-2024-1234")

    print("Mapped Techniques:", techniques)
    print("\nAttack Chain Analysis:")
    analysis = engine.analyze_attack_chain(techniques)
    print(f"  Risk Level: {analysis['risk_level']}")
    print(f"  Attack Flow: {analysis['potential_flow']}")

    engine.export_matrix_json("mitre_matrix.json")
    print("\nMatrix exported to mitre_matrix.json")
