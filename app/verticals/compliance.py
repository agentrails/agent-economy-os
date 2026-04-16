from app.verticals.base import CredentialPack, CredentialDefinition
from typing import Dict, Any, List
import time
from datetime import datetime, timezone

def export_audit_report(agent_id: str) -> Dict[str, Any]:
    """
    Generates an auditor-ready export of the agent's recent proxy execution logs.
    Reuses the existing analytics/metering layer to gather the data.
    """
    from app.analytics import get_analytics_stats
    
    stats = get_analytics_stats()
    recent_activity = stats.get("recent_activity", [])
    
    # Filter for the specific agent
    agent_activity = [event for event in recent_activity if event.get("agent_id") == agent_id]
    
    return {
        "report_id": f"rep_{int(time.time())}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "total_events_exported": len(agent_activity),
        "events": agent_activity,
        "certification": "Auditor-Ready Export - Universal Agent Economy OS"
    }

ComplianceCredentialPack = CredentialPack(
    pack_id="compliance",
    name="Compliance & Governance",
    description="Enterprise-grade credentials for audit logging, KYC, regulatory reporting, and smart contract audits.",
    credentials={
        "audit_log_access": CredentialDefinition(
            name="Audit Log Access",
            description="Read-only access to immutable transaction and proxy execution audit logs.",
            allowed_scopes=["audit:read", "audit:export"]
        ),
        "audit_report_generator": CredentialDefinition(
            name="Audit Report Generator",
            description="Capability to generate auditor-ready export reports of proxy execution logs.",
            allowed_scopes=["audit:export", "report:generate"]
        ),
        "kyc_verification": CredentialDefinition(
            name="KYC Verification Provider",
            description="Credentials for third-party Know Your Customer (KYC) and AML verification services.",
            allowed_scopes=["kyc:verify", "identity:verify"]
        ),
        "regulatory_reporting": CredentialDefinition(
            name="Regulatory Reporting API",
            description="Access to automated tax and regulatory reporting endpoints.",
            allowed_scopes=["report:generate", "report:submit"]
        ),
        "smart_contract_audit": CredentialDefinition(
            name="Smart Contract Auditor",
            description="Access to automated smart contract vulnerability scanning and formal verification tools.",
            allowed_scopes=["contract:scan", "contract:verify"]
        ),
        "gdpr_compliance": CredentialDefinition(
            name="GDPR Data Controller",
            description="Credentials for managing data subject access requests and right-to-be-forgotten operations.",
            allowed_scopes=["data:delete", "data:export", "consent:manage"]
        )
    }
)
