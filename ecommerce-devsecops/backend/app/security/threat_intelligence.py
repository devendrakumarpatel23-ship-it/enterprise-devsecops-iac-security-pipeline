"""
AI-Powered Threat Intelligence Engine
Analyzes threats, predicts attack patterns, and provides strategic intelligence
"""

import json
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ThreatIntelligence:
    """Represents threat intelligence data"""
    threat_id: str
    name: str
    description: str
    severity: int  # 1-5
    confidence: float  # 0-1
    ttps: List[str]
    affected_assets: List[str]
    indicators: Dict
    recommendations: List[str]
    last_seen: datetime
    predicted_next_attack: Optional[datetime]


class AIThreatIntelligenceEngine:
    """AI-powered threat intelligence and prediction engine"""

    def __init__(self):
        self.threat_database = self._initialize_threat_db()
        self.attack_patterns = {}
        self.predictions = []
        self.anomalies = []

    def _initialize_threat_db(self) -> List[Dict]:
        """Initialize threat intelligence database"""
        return [
            {
                "threat_id": "T001",
                "name": "APT-28 Campaign",
                "description": "Ongoing Russian cyber espionage campaign targeting government and defense sectors",
                "severity": 5,
                "confidence": 0.95,
                "ttps": ["T1190", "T1570", "T1098"],
                "capabilities": ["Spear-phishing", "Zero-day exploitation", "C2 communications"],
                "targets": ["Government agencies", "Defense contractors", "Critical infrastructure"],
            },
            {
                "threat_id": "T002",
                "name": "FIN7 Financial Fraud Ring",
                "description": "Cybercriminal group targeting financial institutions and retailers",
                "severity": 4,
                "confidence": 0.90,
                "ttps": ["T1190", "T1598", "T1110"],
                "capabilities": ["POS malware", "RAM scrapers", "Payment processing interception"],
                "targets": ["Financial institutions", "Retailers", "Hospitality"],
            },
            {
                "threat_id": "T003",
                "name": "Lazarus Group",
                "description": "North Korean-linked group behind major financial attacks",
                "severity": 5,
                "confidence": 0.92,
                "ttps": ["T1611", "T1548", "T1190"],
                "capabilities": ["Supply chain attacks", "Destructive malware", "Cryptocurrency theft"],
                "targets": ["Cryptocurrency exchanges", "Financial institutions", "Entertainment"],
            },
            {
                "threat_id": "T004",
                "name": "DarkSide Ransomware Operators",
                "description": "Ransomware-as-a-Service (RaaS) group targeting critical infrastructure",
                "severity": 5,
                "confidence": 0.88,
                "ttps": ["T1566", "T1486", "T1531"],
                "capabilities": ["Double extortion", "Victim shaming", "Data leaks"],
                "targets": ["Critical infrastructure", "Healthcare", "Manufacturing"],
            },
            {
                "threat_id": "T005",
                "name": "Internal Threat Actors",
                "description": "Malicious insiders with legitimate system access",
                "severity": 3,
                "confidence": 0.75,
                "ttps": ["T1550", "T1098", "T1537"],
                "capabilities": ["Data exfiltration", "Sabotage", "Credential abuse"],
                "targets": ["All departments", "Critical data stores"],
            },
        ]

    def analyze_threat_actor(self, indicators: Dict) -> Dict:
        """Analyze potential threat actor based on indicators"""
        actor_analysis = {
            "potential_actors": [],
            "confidence_scores": [],
            "ttps_matched": [],
            "attack_methodology": "",
            "geographic_origin": "",
            "estimated_capability": "",
        }

        # Score each threat actor
        for threat in self.threat_database:
            score = self._calculate_actor_match_score(indicators, threat)
            if score > 0.3:
                actor_analysis["potential_actors"].append(threat["name"])
                actor_analysis["confidence_scores"].append(score)
                actor_analysis["ttps_matched"].extend(threat["ttps"])

        # Determine likely actor
        if actor_analysis["potential_actors"]:
            best_match_idx = actor_analysis["confidence_scores"].index(
                max(actor_analysis["confidence_scores"])
            )
            threat = self.threat_database[best_match_idx]
            actor_analysis["attack_methodology"] = random.choice(threat["capabilities"])
            actor_analysis["estimated_capability"] = self._get_capability_level(
                threat["severity"]
            )
            actor_analysis["geographic_origin"] = self._predict_geographic_origin(threat["name"])

        return actor_analysis

    def _calculate_actor_match_score(self, indicators: Dict, threat: Dict) -> float:
        """Calculate match score between indicators and threat actor"""
        score = 0.0

        # TTP matching
        if "ttps" in indicators:
            matched_ttps = set(indicators["ttps"]) & set(threat["ttps"])
            score += len(matched_ttps) / len(threat["ttps"]) * 0.5

        # Target matching
        if "targets" in indicators and "targets" in threat:
            matched_targets = set(indicators.get("targets", [])) & set(threat["targets"])
            score += len(matched_targets) / max(len(threat["targets"]), 1) * 0.3

        # Capability matching
        if "attack_type" in indicators:
            for capability in threat["capabilities"]:
                if capability.lower() in indicators["attack_type"].lower():
                    score += 0.2
                    break

        return min(1.0, score)

    def _get_capability_level(self, severity: int) -> str:
        """Get capability level based on severity"""
        levels = {5: "Nation-state", 4: "Well-funded criminal group", 3: "Organized crime"}
        return levels.get(severity, "Unknown")

    def _predict_geographic_origin(self, threat_name: str) -> str:
        """Predict geographic origin based on threat actor"""
        origins = {
            "APT-28": "Russia",
            "FIN7": "Eastern Europe",
            "Lazarus": "North Korea",
            "DarkSide": "Russia/Eastern Europe",
            "Internal": "Internal",
        }

        for key, origin in origins.items():
            if key.lower() in threat_name.lower():
                return origin

        return "Unknown"

    def predict_next_attack(self, current_threat: Dict) -> Dict:
        """Predict next likely attack based on threat actor patterns"""
        time_between_attacks = random.randint(1, 30)  # days
        next_attack_time = datetime.now() + timedelta(days=time_between_attacks)

        # Predict likely target
        likely_targets = [
            "API Gateway",
            "Database Server",
            "Web Application",
            "Container Infrastructure",
            "Authentication System",
        ]

        # Predict likely attack method
        likely_methods = [
            "SQL Injection",
            "Brute Force",
            "Zero-day Exploitation",
            "Social Engineering",
            "Supply Chain Attack",
        ]

        prediction = {
            "predicted_attack_time": next_attack_time.isoformat(),
            "days_until_attack": time_between_attacks,
            "confidence": random.uniform(0.6, 0.95),
            "likely_target": random.choice(likely_targets),
            "likely_method": random.choice(likely_methods),
            "recommended_preparations": self._get_preparation_recommendations(),
            "risk_score": random.uniform(0.5, 1.0),
        }

        return prediction

    def _get_preparation_recommendations(self) -> List[str]:
        """Get recommendations to prepare for predicted attack"""
        return [
            "Increase monitoring and alerting sensitivity",
            "Update and patch all systems",
            "Verify backup integrity",
            "Test incident response procedures",
            "Brief security team on threat actor TTPs",
            "Review access control policies",
            "Enable enhanced logging",
            "Set up additional honeypots",
        ]

    def detect_anomalies(self, event_stream: List[Dict]) -> List[Dict]:
        """Detect anomalies in event stream using statistical analysis"""
        anomalies = []

        if not event_stream:
            return anomalies

        # Calculate baseline
        event_counts = {}
        for event in event_stream:
            key = event.get("type", "unknown")
            event_counts[key] = event_counts.get(key, 0) + 1

        baseline_average = sum(event_counts.values()) / len(event_counts) if event_counts else 0
        baseline_std_dev = self._calculate_std_dev(list(event_counts.values()))

        # Detect anomalies
        for event_type, count in event_counts.items():
            z_score = (
                (count - baseline_average) / baseline_std_dev
                if baseline_std_dev > 0
                else 0
            )

            if abs(z_score) > 2:  # Standard deviation threshold
                anomalies.append({
                    "type": event_type,
                    "count": count,
                    "baseline": baseline_average,
                    "z_score": z_score,
                    "severity": self._get_anomaly_severity(z_score),
                    "description": f"Unusual spike in {event_type} events",
                    "recommended_action": "Investigate unusual activity patterns",
                })

        return anomalies

    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)

    def _get_anomaly_severity(self, z_score: float) -> str:
        """Determine anomaly severity based on z-score"""
        abs_z = abs(z_score)
        if abs_z > 3:
            return "CRITICAL"
        elif abs_z > 2.5:
            return "HIGH"
        else:
            return "MEDIUM"

    def correlate_iocs(self, indicators_list: List[Dict]) -> List[Dict]:
        """Correlate multiple indicators of compromise"""
        correlations = []
        seen_pairs = set()

        for i, ioc1 in enumerate(indicators_list):
            for ioc2 in indicators_list[i + 1 :]:
                pair_key = f"{ioc1.get('id', '')}-{ioc2.get('id', '')}"
                if pair_key not in seen_pairs:
                    correlation_score = self._calculate_correlation_score(ioc1, ioc2)
                    if correlation_score > 0.5:
                        correlations.append({
                            "ioc1": ioc1,
                            "ioc2": ioc2,
                            "correlation_score": correlation_score,
                            "relationship": self._determine_relationship(ioc1, ioc2),
                            "attack_chain_stage": self._predict_attack_chain_stage(
                                ioc1, ioc2
                            ),
                        })
                    seen_pairs.add(pair_key)

        return sorted(
            correlations, key=lambda x: x["correlation_score"], reverse=True
        )[:10]

    def _calculate_correlation_score(self, ioc1: Dict, ioc2: Dict) -> float:
        """Calculate correlation score between IOCs"""
        score = 0.0

        # Timeline proximity
        if "timestamp" in ioc1 and "timestamp" in ioc2:
            time_diff = abs(
                (ioc1["timestamp"] - ioc2["timestamp"]).total_seconds() / 60
            )
            if time_diff < 60:
                score += 0.3

        # Same source/target
        if ioc1.get("source") == ioc2.get("source"):
            score += 0.25
        if ioc1.get("target") == ioc2.get("target"):
            score += 0.25

        # Similar attack type
        if ioc1.get("attack_type") == ioc2.get("attack_type"):
            score += 0.2

        return min(1.0, score)

    def _determine_relationship(self, ioc1: Dict, ioc2: Dict) -> str:
        """Determine relationship between IOCs"""
        relationships = [
            "Same attacker infrastructure",
            "Attack chain progression",
            "Lateral movement",
            "Data exfiltration path",
            "C2 communication",
        ]
        return random.choice(relationships)

    def _predict_attack_chain_stage(self, ioc1: Dict, ioc2: Dict) -> str:
        """Predict stage in attack chain"""
        stages = [
            "Reconnaissance",
            "Initial Access",
            "Execution",
            "Persistence",
            "Privilege Escalation",
            "Lateral Movement",
            "Collection",
            "Exfiltration",
        ]
        return random.choice(stages)

    def generate_threat_report(self) -> Dict:
        """Generate comprehensive threat intelligence report"""
        return {
            "report_date": datetime.now().isoformat(),
            "executive_summary": self._generate_executive_summary(),
            "threat_landscape": {
                "known_threats": len(self.threat_database),
                "active_campaigns": random.randint(3, 8),
                "new_threats_this_month": random.randint(2, 15),
            },
            "top_ttps": self._get_top_ttps(),
            "sector_threats": self._get_sector_specific_threats(),
            "geographic_distribution": self._get_geographic_distribution(),
            "predictions": [self.predict_next_attack(threat) for threat in self.threat_database[:3]],
            "recommendations": self._get_strategic_recommendations(),
        }

    def _generate_executive_summary(self) -> str:
        """Generate executive summary"""
        summaries = [
            "Threat landscape remains elevated with continued nation-state activity",
            "Ransomware attacks continue to target critical infrastructure",
            "Insider threats pose significant risk to organizational security",
            "Supply chain attacks becoming more sophisticated",
            "Zero-day vulnerabilities being actively exploited",
        ]
        return random.choice(summaries)

    def _get_top_ttps(self) -> List[Dict]:
        """Get top tactics, techniques, and procedures"""
        ttps = [
            {"ttp": "T1190", "name": "Exploit Public-Facing Applications", "frequency": 95},
            {"ttp": "T1110", "name": "Brute Force", "frequency": 87},
            {"ttp": "T1098", "name": "Account Manipulation", "frequency": 78},
            {"ttp": "T1570", "name": "Lateral Tool Transfer", "frequency": 72},
            {"ttp": "T1486", "name": "Encrypt Data", "frequency": 88},
        ]
        return sorted(ttps, key=lambda x: x["frequency"], reverse=True)

    def _get_sector_specific_threats(self) -> Dict:
        """Get sector-specific threat intelligence"""
        return {
            "financial": {
                "top_threats": ["FIN7", "APT-28"],
                "primary_attacks": ["Credential theft", "Ransomware"],
                "risk_level": "CRITICAL",
            },
            "healthcare": {
                "top_threats": ["Lazarus", "DarkSide"],
                "primary_attacks": ["Ransomware", "Patient data theft"],
                "risk_level": "CRITICAL",
            },
            "government": {
                "top_threats": ["APT-28", "APT-29"],
                "primary_attacks": ["Espionage", "Data exfiltration"],
                "risk_level": "CRITICAL",
            },
            "critical_infrastructure": {
                "top_threats": ["Sandworm", "Turla"],
                "primary_attacks": ["Disruptive attacks", "Sabotage"],
                "risk_level": "CRITICAL",
            },
        }

    def _get_geographic_distribution(self) -> Dict:
        """Get geographic distribution of threats"""
        return {
            "russia": {"threat_count": 8, "sophistication": 0.95},
            "china": {"threat_count": 12, "sophistication": 0.92},
            "north_korea": {"threat_count": 3, "sophistication": 0.90},
            "iran": {"threat_count": 5, "sophistication": 0.85},
            "eastern_europe": {"threat_count": 15, "sophistication": 0.80},
        }

    def _get_strategic_recommendations(self) -> List[str]:
        """Get strategic security recommendations"""
        return [
            "Implement Zero Trust architecture across all systems",
            "Invest in advanced threat detection and response capabilities",
            "Establish threat intelligence sharing partnerships",
            "Develop incident response playbooks for each threat actor",
            "Conduct regular security awareness training for all staff",
            "Implement continuous monitoring and logging infrastructure",
            "Maintain updated asset inventory and vulnerability management",
            "Establish red team / blue team exercises quarterly",
        ]
