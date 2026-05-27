"""
Realistic Attack Simulation Generator
Generates enterprise-grade attack simulations with realistic event sequences
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class AttackScenario:
    """Represents a realistic attack scenario"""
    scenario_id: str
    name: str
    description: str
    threat_actor: str
    attack_chain: List[Dict]
    indicators_of_compromise: List[str]
    ttps: List[str]  # Tactics, Techniques, Procedures
    estimated_impact: str


class AttackGenerator:
    """Generates realistic attack scenarios"""

    def __init__(self):
        self.attack_patterns = self._initialize_attack_patterns()

    def _initialize_attack_patterns(self) -> Dict:
        """Initialize realistic attack patterns"""
        return {
            "sql_injection": {
                "stages": [
                    {
                        "name": "Reconnaissance",
                        "actions": [
                            "Probe API endpoints for SQL injection points",
                            "Enumerate database structure",
                            "Identify authentication mechanisms",
                        ],
                        "indicators": [
                            "Multiple 400/403 HTTP responses",
                            "Unusual SQL keywords in requests",
                            "High request rate to /api/users endpoint",
                        ],
                    },
                    {
                        "name": "Exploitation",
                        "actions": [
                            "Execute SQL injection payload",
                            "Extract sensitive data",
                            "Dump user credentials",
                        ],
                        "indicators": [
                            "SQL error messages in response",
                            "Large response sizes from API",
                            "Unusual queries in database logs",
                        ],
                    },
                    {
                        "name": "Exfiltration",
                        "actions": [
                            "Transmit stolen data to C2 server",
                            "Encode data in DNS queries",
                            "Use HTTPS to mask traffic",
                        ],
                        "indicators": [
                            "DNS queries to suspicious domains",
                            "High volume outbound traffic",
                            "Connections to known C2 IPs",
                        ],
                    },
                ],
                "ttps": ["T1190", "T1046", "T1583"],
            },
            "brute_force": {
                "stages": [
                    {
                        "name": "Enumeration",
                        "actions": [
                            "Identify valid usernames",
                            "Enumerate user accounts",
                            "Test default credentials",
                        ],
                        "indicators": [
                            "High volume of 401 responses",
                            "Multiple failed login attempts",
                            "Same username from different IPs",
                        ],
                    },
                    {
                        "name": "Attack",
                        "actions": [
                            "Execute brute force attack",
                            "Test common passwords",
                            "Use password spray technique",
                        ],
                        "indicators": [
                            "1000+ failed login attempts per minute",
                            "Account lockout events",
                            "Login attempts across multiple accounts",
                        ],
                    },
                    {
                        "name": "Access",
                        "actions": [
                            "Successful login to admin account",
                            "Bypass MFA if configured",
                            "Establish persistence",
                        ],
                        "indicators": [
                            "Successful login from unusual location",
                            "Session token exfiltration",
                            "Privilege escalation activities",
                        ],
                    },
                ],
                "ttps": ["T1110", "T1078", "T1555"],
            },
            "container_escape": {
                "stages": [
                    {
                        "name": "Compromise",
                        "actions": [
                            "Compromise containerized application",
                            "Gain shell access in container",
                            "Enumerate container runtime",
                        ],
                        "indicators": [
                            "Unusual process execution in container",
                            "Reverse shell connections",
                            "Container privilege escalation attempts",
                        ],
                    },
                    {
                        "name": "Exploitation",
                        "actions": [
                            "Exploit container runtime vulnerability",
                            "Mount host filesystem",
                            "Escape to host system",
                        ],
                        "indicators": [
                            "System calls to escape containers",
                            "Host filesystem access from container",
                            "Docker daemon exploitation attempts",
                        ],
                    },
                    {
                        "name": "Persistence",
                        "actions": [
                            "Install rootkit on host",
                            "Create hidden processes",
                            "Establish C2 communication",
                        ],
                        "indicators": [
                            "Kernel module loading",
                            "System service modifications",
                            "Persistence mechanisms detected",
                        ],
                    },
                ],
                "ttps": ["T1611", "T1548", "T1547"],
            },
            "lateral_movement": {
                "stages": [
                    {
                        "name": "Discovery",
                        "actions": [
                            "Enumerate network resources",
                            "Discover service accounts",
                            "Map network topology",
                        ],
                        "indicators": [
                            "Network scan activity",
                            "Unusual LDAP queries",
                            "Service discovery attempts",
                        ],
                    },
                    {
                        "name": "Credential_Access",
                        "actions": [
                            "Extract cached credentials",
                            "Harvest hashes from memory",
                            "Use credential stuffing",
                        ],
                        "indicators": [
                            "Registry access patterns",
                            "Memory dumping tools detected",
                            "Credential manager access",
                        ],
                    },
                    {
                        "name": "Lateral_Movement",
                        "actions": [
                            "Use stolen credentials",
                            "Move to adjacent systems",
                            "Escalate privileges laterally",
                        ],
                        "indicators": [
                            "Lateral tool transfer",
                            "Pass-the-hash attacks",
                            "Unusual cross-system authentication",
                        ],
                    },
                ],
                "ttps": ["T1570", "T1550", "T1021"],
            },
            "ransomware": {
                "stages": [
                    {
                        "name": "Delivery",
                        "actions": [
                            "Send phishing email with malware",
                            "Exploit vulnerable application",
                            "Social engineering attack",
                        ],
                        "indicators": [
                            "Suspicious email attachment opened",
                            "Malicious download initiated",
                            "Process injection detected",
                        ],
                    },
                    {
                        "name": "Execution",
                        "actions": [
                            "Execute ransomware payload",
                            "Establish persistence",
                            "Disable security tools",
                        ],
                        "indicators": [
                            "Suspicious process execution",
                            "Antivirus/EDR disabling attempts",
                            "Scheduled task creation",
                        ],
                    },
                    {
                        "name": "Encryption",
                        "actions": [
                            "Enumerate accessible files",
                            "Encrypt critical data",
                            "Generate ransom note",
                        ],
                        "indicators": [
                            "High disk I/O activity",
                            "Cryptographic operations",
                            "File modification events",
                        ],
                    },
                ],
                "ttps": ["T1566", "T1486", "T1531"],
            },
            "xss_attack": {
                "stages": [
                    {
                        "name": "Reconnaissance",
                        "actions": [
                            "Identify XSS vulnerable endpoints",
                            "Test input validation",
                            "Map application attack surface",
                        ],
                        "indicators": [
                            "Unusual request parameters",
                            "Script injection attempts",
                            "Multiple 400/422 responses",
                        ],
                    },
                    {
                        "name": "Exploitation",
                        "actions": [
                            "Inject malicious JavaScript",
                            "Steal user session tokens",
                            "Redirect users to phishing site",
                        ],
                        "indicators": [
                            "Script tags in API responses",
                            "XSS payload in logs",
                            "Abnormal client-side activity",
                        ],
                    },
                    {
                        "name": "Persistence",
                        "actions": [
                            "Store payload in database",
                            "Maintain backdoor access",
                            "Monitor for session hijacking",
                        ],
                        "indicators": [
                            "Malicious entries in database",
                            "Persistent XSS payloads",
                            "Session cookie exfiltration",
                        ],
                    },
                ],
                "ttps": ["T1598", "T1566", "T1113"],
            },
        }

    def generate_attack_timeline(self, attack_type: str, duration_minutes: int = 60) -> List[Dict]:
        """Generate realistic attack timeline"""
        if attack_type not in self.attack_patterns:
            attack_type = random.choice(list(self.attack_patterns.keys()))

        pattern = self.attack_patterns[attack_type]
        events = []
        now = datetime.now()
        current_time = now - timedelta(minutes=duration_minutes)

        for stage in pattern["stages"]:
            stage_duration = duration_minutes // len(pattern["stages"])
            for _ in range(random.randint(2, 5)):
                event = {
                    "timestamp": current_time.isoformat(),
                    "stage": stage["name"],
                    "action": random.choice(stage["actions"]),
                    "indicator": random.choice(stage["indicators"]),
                    "severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
                }
                events.append(event)
                current_time += timedelta(minutes=random.randint(1, 5))

        return events

    def generate_ioc_report(self, attack_type: str) -> Dict:
        """Generate Indicators of Compromise report"""
        pattern = self.attack_patterns.get(
            attack_type, list(self.attack_patterns.values())[0]
        )

        iocs = {
            "ips": [
                f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                for _ in range(random.randint(2, 5))
            ],
            "domains": [
                f"malicious-domain-{random.randint(1000, 9999)}.com",
                f"c2-server-{random.randint(1000, 9999)}.net",
                f"exfil-{random.randint(1000, 9999)}.xyz",
            ],
            "file_hashes": [
                "".join(random.choices("0123456789abcdef", k=64))
                for _ in range(random.randint(1, 3))
            ],
            "urls": [
                f"http://malicious.com/payload{random.randint(1, 100)}",
                f"http://c2-server.net/command?id={random.randint(1, 100000)}",
            ],
            "process_names": [
                "svchost.exe",
                "explorer.exe",
                "rundll32.exe",
                "powershell.exe",
            ],
            "registry_keys": [
                "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
            ],
        }

        return {
            "attack_type": attack_type,
            "generated_at": datetime.now().isoformat(),
            "iocs": iocs,
            "ttps": pattern["ttps"],
            "recommendations": self._generate_ioc_recommendations(attack_type),
        }

    def _generate_ioc_recommendations(self, attack_type: str) -> List[str]:
        """Generate remediation recommendations based on attack type"""
        recommendations = {
            "sql_injection": [
                "Use parameterized queries / prepared statements",
                "Implement WAF rules for SQL injection",
                "Validate and sanitize all user inputs",
                "Apply principle of least privilege to database accounts",
                "Enable SQL query logging and monitoring",
            ],
            "brute_force": [
                "Enforce strong password policies",
                "Implement multi-factor authentication",
                "Use account lockout policies",
                "Deploy rate limiting on authentication endpoints",
                "Monitor and alert on failed login attempts",
            ],
            "container_escape": [
                "Keep container runtimes updated",
                "Use read-only root filesystems",
                "Drop unnecessary Linux capabilities",
                "Implement runtime security monitoring",
                "Use network policies to restrict container communication",
            ],
            "lateral_movement": [
                "Implement network segmentation",
                "Use endpoint detection and response (EDR)",
                "Monitor lateral movement indicators",
                "Enforce service account management",
                "Disable pass-the-hash attacks",
            ],
            "ransomware": [
                "Maintain encrypted, offline backups",
                "Deploy and monitor EDR solutions",
                "Block known ransomware file extensions",
                "Restrict administrative privileges",
                "Enable immutable logging and monitoring",
            ],
            "xss_attack": [
                "Implement Content Security Policy (CSP)",
                "Sanitize and validate all inputs",
                "Use template engines with auto-escaping",
                "Apply output encoding",
                "Regular security testing for XSS vulnerabilities",
            ],
        }

        return recommendations.get(attack_type, ["Implement general security best practices"])

    def generate_simulated_logs(self, attack_type: str, count: int = 100) -> List[Dict]:
        """Generate simulated security logs for an attack"""
        logs = []
        now = datetime.now()

        for i in range(count):
            timestamp = now - timedelta(seconds=random.randint(0, 3600))
            log = {
                "timestamp": timestamp.isoformat(),
                "log_type": random.choice(["FIREWALL", "IDS", "WAF", "SIEM", "EDR"]),
                "event_id": f"{random.randint(1000, 9999)}",
                "severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
                "source_ip": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "destination_ip": f"10.0.{random.randint(0,255)}.{random.randint(0,255)}",
                "message": self._generate_log_message(attack_type),
                "raw_data": self._generate_raw_log_data(attack_type),
            }
            logs.append(log)

        return sorted(logs, key=lambda x: x["timestamp"])

    def _generate_log_message(self, attack_type: str) -> str:
        """Generate realistic log message"""
        messages = {
            "sql_injection": [
                "SQL Injection attempt detected in parameter 'id'",
                "Suspicious SQL keywords in request body",
                "Database error revealed in response",
            ],
            "brute_force": [
                "Multiple failed authentication attempts from single IP",
                "Account lockout triggered after 5 failed attempts",
                "Password spray attack detected",
            ],
            "container_escape": [
                "Privileged container escape attempt detected",
                "Unusual system call from container detected",
                "Host filesystem access from container",
            ],
            "lateral_movement": [
                "Lateral tool transfer detected",
                "Credential harvesting activity detected",
                "Pass-the-hash attack detected",
            ],
            "ransomware": [
                "Suspicious file encryption activity detected",
                "Ransomware process detected and quarantined",
                "Malware signature matched: Ransomware.Generic",
            ],
            "xss_attack": [
                "XSS payload detected in request",
                "Script injection attempt blocked by WAF",
                "DOM-based XSS vulnerability exploited",
            ],
        }

        return random.choice(messages.get(attack_type, ["Security event detected"]))

    def _generate_raw_log_data(self, attack_type: str) -> Dict:
        """Generate realistic raw log data"""
        return {
            "user_agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "curl/7.64.1",
                "Python-Requests/2.25.1",
            ]),
            "request_method": random.choice(["GET", "POST", "PUT", "DELETE"]),
            "status_code": random.choice([400, 403, 500, 503]),
            "response_time_ms": random.randint(1, 5000),
            "bytes_sent": random.randint(100, 100000),
            "bytes_received": random.randint(100, 50000),
        }

    def get_attack_summary(self, attack_type: str) -> Dict:
        """Get comprehensive attack summary"""
        pattern = self.attack_patterns.get(
            attack_type, list(self.attack_patterns.values())[0]
        )

        return {
            "attack_type": attack_type,
            "description": f"Simulated {attack_type.replace('_', ' ').title()} Attack",
            "stages": len(pattern["stages"]),
            "estimated_duration_minutes": random.randint(30, 480),
            "threat_level": random.choice(["HIGH", "CRITICAL"]),
            "ttps": pattern["ttps"],
            "timeline": self.generate_attack_timeline(attack_type),
            "iocs": self.generate_ioc_report(attack_type),
            "sample_logs": self.generate_simulated_logs(attack_type, 20),
        }
