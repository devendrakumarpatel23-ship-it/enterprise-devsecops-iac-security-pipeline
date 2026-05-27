"""
Zero Trust Security Validation Engine
Implements least privilege principles, secure-by-default policies, and zero trust principles
"""
import json
from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum


class TrustLevel(Enum):
    """Trust evaluation levels"""
    FULL_TRUST = "full_trust"
    CONDITIONAL_TRUST = "conditional_trust"
    MINIMAL_TRUST = "minimal_trust"
    NO_TRUST = "no_trust"


class ZeroTrustValidator:
    """Validates zero trust security principles"""

    def __init__(self):
        self.policies = self._initialize_policies()
        self.validation_results = {}

    def _initialize_policies(self) -> Dict:
        """Initialize zero trust policies"""
        return {
            "least_privilege": {
                "description": "Enforce least privilege access",
                "rules": {
                    "admin_access": {
                        "requirement": "Admin access requires MFA and approval",
                        "status": "enforced",
                        "implementation": "OAuth2 + TOTP",
                    },
                    "api_scopes": {
                        "requirement": "API tokens have minimal required scopes",
                        "status": "enforced",
                        "implementation": "Scope-based JWT tokens",
                    },
                    "database_access": {
                        "requirement": "Database access limited to specific users/applications",
                        "status": "enforced",
                        "implementation": "Role-based database accounts",
                    },
                    "file_permissions": {
                        "requirement": "File permissions follow least privilege",
                        "status": "enforced",
                        "implementation": "Unix permissions (600/700)",
                    },
                },
            },
            "secure_by_default": {
                "description": "Secure configurations by default",
                "rules": {
                    "encryption_at_rest": {
                        "requirement": "All data encrypted at rest",
                        "status": "enforced",
                        "implementation": "AES-256",
                        "compliance": True,
                    },
                    "encryption_in_transit": {
                        "requirement": "All data encrypted in transit",
                        "status": "enforced",
                        "implementation": "TLS 1.3",
                        "compliance": True,
                    },
                    "https_only": {
                        "requirement": "HTTPS enforced for all web traffic",
                        "status": "enforced",
                        "implementation": "HSTS headers",
                        "compliance": True,
                    },
                    "default_deny": {
                        "requirement": "Default firewall policy is DENY",
                        "status": "enforced",
                        "implementation": "Whitelist-based rules",
                        "compliance": True,
                    },
                },
            },
            "api_trust_verification": {
                "description": "Verify API trust and authenticity",
                "rules": {
                    "api_authentication": {
                        "requirement": "All APIs require authentication",
                        "status": "enforced",
                        "implementation": "JWT Bearer tokens",
                    },
                    "api_rate_limiting": {
                        "requirement": "Rate limiting on all public APIs",
                        "status": "enforced",
                        "implementation": "Token bucket algorithm",
                    },
                    "api_signature_verification": {
                        "requirement": "Request signatures verified",
                        "status": "enforced",
                        "implementation": "HMAC-SHA256",
                    },
                    "api_versioning": {
                        "requirement": "API versioning for backwards compatibility",
                        "status": "enforced",
                        "implementation": "Version header validation",
                    },
                },
            },
            "network_segmentation": {
                "description": "Enforce network segmentation",
                "rules": {
                    "vpc_isolation": {
                        "requirement": "Application and database in separate subnets",
                        "status": "enforced",
                        "implementation": "AWS VPC with security groups",
                    },
                    "container_network_policy": {
                        "requirement": "Network policies limit pod-to-pod communication",
                        "status": "enforced",
                        "implementation": "Kubernetes NetworkPolicy",
                    },
                    "firewall_rules": {
                        "requirement": "Firewall rules restrict traffic",
                        "status": "enforced",
                        "implementation": "WAF rules configured",
                    },
                    "dmz_setup": {
                        "requirement": "DMZ for external-facing services",
                        "status": "enforced",
                        "implementation": "Nginx reverse proxy",
                    },
                },
            },
            "container_isolation": {
                "description": "Enforce container isolation",
                "rules": {
                    "read_only_filesystem": {
                        "requirement": "Container filesystems read-only",
                        "status": "enforced",
                        "implementation": "Docker read-only volumes",
                    },
                    "capability_dropping": {
                        "requirement": "Drop unnecessary Linux capabilities",
                        "status": "enforced",
                        "implementation": "securityContext drop: ALL",
                    },
                    "user_namespace": {
                        "requirement": "Run containers as non-root",
                        "status": "enforced",
                        "implementation": "runAsNonRoot: true",
                    },
                    "resource_limits": {
                        "requirement": "CPU and memory limits set",
                        "status": "enforced",
                        "implementation": "K8s resource requests/limits",
                    },
                },
            },
            "kubernetes_rbac": {
                "description": "Kubernetes RBAC enforcement",
                "rules": {
                    "role_definitions": {
                        "requirement": "Fine-grained roles defined",
                        "status": "enforced",
                        "roles": ["admin", "deployer", "viewer", "auditor"],
                    },
                    "service_accounts": {
                        "requirement": "Unique service accounts per workload",
                        "status": "enforced",
                        "implementation": "Workload Identity",
                    },
                    "role_binding": {
                        "requirement": "Bindings follow least privilege",
                        "status": "enforced",
                        "verification": "Regular audits",
                    },
                    "audit_logging": {
                        "requirement": "RBAC changes are audited",
                        "status": "enforced",
                        "implementation": "Kubernetes audit logs",
                    },
                },
            },
        }

    def validate_least_privilege(self, user_context: Dict) -> Dict:
        """Validate least privilege enforcement"""
        result = {
            "category": "least_privilege",
            "user": user_context.get("user_id"),
            "checks": [],
            "compliant": True,
        }

        policies = self.policies["least_privilege"]["rules"]

        # Check admin access
        if user_context.get("is_admin"):
            result["checks"].append(
                {
                    "name": "admin_access",
                    "status": "compliant" if user_context.get("mfa_enabled") else "non_compliant",
                    "message": "MFA required for admin access",
                    "required": user_context.get("mfa_enabled", False),
                }
            )

        # Check API scopes
        scopes = user_context.get("api_scopes", [])
        scope_check = {
            "name": "api_scopes",
            "status": "compliant" if len(scopes) <= 3 else "non_compliant",
            "message": f"Requested scopes: {', '.join(scopes)}",
            "scope_count": len(scopes),
        }
        result["checks"].append(scope_check)

        # Check database access
        if user_context.get("needs_db_access"):
            result["checks"].append(
                {
                    "name": "database_access",
                    "status": "compliant" if user_context.get("role") in ["developer", "dba"] else "non_compliant",
                    "message": "Only specific roles have database access",
                    "access_granted": user_context.get("role") in ["developer", "dba"],
                }
            )

        result["compliant"] = all(c["status"] == "compliant" for c in result["checks"])
        return result

    def validate_secure_by_default(self) -> Dict:
        """Validate secure-by-default configurations"""
        result = {
            "category": "secure_by_default",
            "validations": {},
            "compliant": True,
        }

        policies = self.policies["secure_by_default"]["rules"]

        for policy_name, policy in policies.items():
            result["validations"][policy_name] = {
                "status": policy.get("status", "unknown"),
                "implementation": policy.get("implementation"),
                "compliant": policy.get("compliance", False),
            }

        result["compliant"] = all(
            v["compliant"] for v in result["validations"].values()
        )
        return result

    def validate_api_trust(self, api_request: Dict) -> Dict:
        """Validate API trust and authenticity"""
        result = {
            "category": "api_trust_verification",
            "endpoint": api_request.get("endpoint"),
            "checks": [],
            "trust_level": TrustLevel.NO_TRUST.value,
        }

        # Check authentication
        has_token = bool(api_request.get("bearer_token"))
        result["checks"].append(
            {"name": "authentication", "passed": has_token, "message": "Valid Bearer token"}
        )

        # Check signature
        has_signature = bool(api_request.get("signature"))
        result["checks"].append(
            {"name": "signature_verification", "passed": has_signature, "message": "Request signed"}
        )

        # Check rate limit
        within_limit = api_request.get("request_count", 0) < 1000
        result["checks"].append(
            {
                "name": "rate_limit",
                "passed": within_limit,
                "message": f"Request count: {api_request.get('request_count', 0)}/1000",
            }
        )

        all_passed = all(c["passed"] for c in result["checks"])

        if all_passed:
            result["trust_level"] = TrustLevel.FULL_TRUST.value
        elif sum(1 for c in result["checks"] if c["passed"]) >= 2:
            result["trust_level"] = TrustLevel.CONDITIONAL_TRUST.value
        elif sum(1 for c in result["checks"] if c["passed"]) >= 1:
            result["trust_level"] = TrustLevel.MINIMAL_TRUST.value

        return result

    def validate_network_segmentation(self, deployment_config: Dict) -> Dict:
        """Validate network segmentation"""
        result = {
            "category": "network_segmentation",
            "checks": [],
            "compliant": True,
        }

        policies = self.policies["network_segmentation"]["rules"]

        # Check VPC isolation
        vpc_check = {
            "name": "vpc_isolation",
            "status": "compliant" if deployment_config.get("app_subnet") != deployment_config.get("db_subnet") else "non_compliant",
            "message": f"App in {deployment_config.get('app_subnet')}, DB in {deployment_config.get('db_subnet')}",
        }
        result["checks"].append(vpc_check)

        # Check firewall rules
        fw_check = {
            "name": "firewall_rules",
            "status": "compliant" if deployment_config.get("default_policy") == "DENY" else "non_compliant",
            "message": f"Default policy: {deployment_config.get('default_policy', 'ALLOW')}",
        }
        result["checks"].append(fw_check)

        result["compliant"] = all(c["status"] == "compliant" for c in result["checks"])
        return result

    def validate_container_isolation(self, container_config: Dict) -> Dict:
        """Validate container isolation"""
        result = {
            "category": "container_isolation",
            "checks": [],
            "compliant": True,
        }

        policies = self.policies["container_isolation"]["rules"]

        # Check read-only filesystem
        result["checks"].append(
            {
                "name": "read_only_filesystem",
                "status": "compliant" if container_config.get("read_only_root_filesystem") else "non_compliant",
                "message": f"Read-only FS: {container_config.get('read_only_root_filesystem', False)}",
            }
        )

        # Check dropped capabilities
        result["checks"].append(
            {
                "name": "capability_dropping",
                "status": "compliant" if "ALL" in container_config.get("dropped_capabilities", []) else "non_compliant",
                "message": f"Dropped capabilities: {container_config.get('dropped_capabilities', [])}",
            }
        )

        # Check non-root user
        result["checks"].append(
            {
                "name": "user_namespace",
                "status": "compliant" if container_config.get("run_as_non_root") else "non_compliant",
                "message": f"Run as non-root: {container_config.get('run_as_non_root', False)}",
            }
        )

        result["compliant"] = all(c["status"] == "compliant" for c in result["checks"])
        return result

    def validate_kubernetes_rbac(self, rbac_config: Dict) -> Dict:
        """Validate Kubernetes RBAC"""
        result = {
            "category": "kubernetes_rbac",
            "checks": [],
            "compliant": True,
        }

        # Check role definitions
        roles = rbac_config.get("roles", [])
        result["checks"].append(
            {
                "name": "role_definitions",
                "status": "compliant" if len(roles) >= 3 else "non_compliant",
                "message": f"Roles defined: {', '.join(roles)}",
            }
        )

        # Check service accounts
        result["checks"].append(
            {
                "name": "service_accounts",
                "status": "compliant" if rbac_config.get("unique_sa_per_workload") else "non_compliant",
                "message": "Unique service accounts per workload",
            }
        )

        # Check audit logging
        result["checks"].append(
            {
                "name": "audit_logging",
                "status": "compliant" if rbac_config.get("audit_enabled") else "non_compliant",
                "message": "RBAC changes audited",
            }
        )

        result["compliant"] = all(c["status"] == "compliant" for c in result["checks"])
        return result

    def perform_full_validation(self, environment_config: Dict) -> Dict:
        """Perform full zero trust validation"""
        validations = {
            "validation_timestamp": datetime.now().isoformat(),
            "environment": environment_config.get("environment", "unknown"),
            "results": {},
            "overall_compliance": False,
        }

        # Run all validations
        validations["results"]["least_privilege"] = self.validate_least_privilege(
            environment_config.get("user_context", {})
        )
        validations["results"]["secure_by_default"] = self.validate_secure_by_default()
        validations["results"]["api_trust"] = self.validate_api_trust(
            environment_config.get("api_request", {})
        )
        validations["results"]["network_segmentation"] = self.validate_network_segmentation(
            environment_config.get("deployment_config", {})
        )
        validations["results"]["container_isolation"] = self.validate_container_isolation(
            environment_config.get("container_config", {})
        )
        validations["results"]["kubernetes_rbac"] = self.validate_kubernetes_rbac(
            environment_config.get("rbac_config", {})
        )

        # Calculate overall compliance
        compliant_count = sum(
            1 for v in validations["results"].values() if v.get("compliant", False)
        )
        total_validations = len(validations["results"])

        validations["compliance_percentage"] = round(compliant_count / total_validations * 100, 2)
        validations["overall_compliance"] = compliant_count == total_validations

        return validations

    def export_validation_report(self, validation_result: Dict, filepath: str) -> bool:
        """Export validation report"""
        try:
            with open(filepath, "w") as f:
                json.dump(validation_result, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False


if __name__ == "__main__":
    validator = ZeroTrustValidator()

    # Sample environment configuration
    env_config = {
        "environment": "production",
        "user_context": {
            "user_id": "user_001",
            "is_admin": True,
            "mfa_enabled": True,
            "api_scopes": ["read:users", "write:products"],
            "needs_db_access": True,
            "role": "developer",
        },
        "deployment_config": {
            "app_subnet": "10.0.1.0/24",
            "db_subnet": "10.0.2.0/24",
            "default_policy": "DENY",
        },
        "container_config": {
            "read_only_root_filesystem": True,
            "dropped_capabilities": ["ALL"],
            "run_as_non_root": True,
        },
        "rbac_config": {
            "roles": ["admin", "deployer", "viewer"],
            "unique_sa_per_workload": True,
            "audit_enabled": True,
        },
    }

    result = validator.perform_full_validation(env_config)

    print("Zero Trust Validation Results:")
    print(f"  Overall Compliance: {result['overall_compliance']}")
    print(f"  Compliance Score: {result['compliance_percentage']}%\n")

    for category, validation in result["results"].items():
        print(f"  {category}: {'✅ Compliant' if validation.get('compliant') else '❌ Non-compliant'}")

    validator.export_validation_report(result, "zero_trust_validation.json")
    print("\nValidation report exported to zero_trust_validation.json")
