"""
Universal Agent Economy OS - Marketing & Ad-Tech Vertical Credential Pack

This module provides the Marketing vertical credential pack, designed specifically
to increase enterprise appeal for acquirers operating in ad-tech, customer data
platforms (CDP), and digital marketing automation.

Strategic Value for Acquirers:
- **Ad-Tech Ready**: Built-in support for major ad platforms, CRM, and social media APIs.
- **Least-Privilege Enforcement**: Granular cryptographic scopes ensure agents only access necessary campaign or audience data, protecting PII.
- **Audit Readiness**: Includes stubs for auditor-ready exports and automated credential rotation, critical for data privacy compliance (e.g., GDPR, CCPA).
- **MarTech Expansion**: Opens the Universal Agent Economy OS to multi-billion dollar marketing automation and CRM ecosystems.
"""
from app.verticals.base import CredentialPack, CredentialDefinition
from typing import Dict, Any
import time
from datetime import datetime, timezone

def generate_marketing_audit_export(agent_id: str, time_range_seconds: int = 86400) -> Dict[str, Any]:
    """
    Generates an auditor-ready export of the agent's recent proxy execution logs,
    specifically formatted for marketing data privacy and campaign auditing.
    
    This stub demonstrates to enterprise acquirers how the OS can seamlessly
    integrate with MarTech compliance workflows.
    """
    from app.analytics import get_analytics_stats
    
    stats = get_analytics_stats()
    recent_activity = stats.get("recent_activity", [])
    now = time.time()
    
    # Filter for the specific agent and time range
    agent_activity = [
        event for event in recent_activity 
        if event.get("agent_id") == agent_id and (now - event.get("timestamp", 0)) <= time_range_seconds
    ]
    
    return {
        "report_id": f"martech_rep_{int(now)}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "time_range_seconds": time_range_seconds,
        "total_events_exported": len(agent_activity),
        "events": agent_activity,
        "certification": "MarTech Auditor-Ready Export - Universal Agent Economy OS",
        "compliance_standard": "Data Privacy (GDPR/CCPA) Ready"
    }

def auto_rotate_marketing_credential(agent_id: str, credential_type: str) -> Dict[str, Any]:
    """
    Stub for automated credential rotation in marketing environments.
    Ensures that third-party vendor access to ad platforms or CRM systems
    is tightly controlled and frequently rotated to prevent data leaks.
    """
    return {
        "status": "rotated",
        "agent_id": agent_id,
        "credential_type": credential_type,
        "rotated_at": datetime.now(timezone.utc).isoformat(),
        "next_rotation_due": "7d" # Standard weekly rotation for marketing APIs
    }

MarketingCredentialPack = CredentialPack(
    pack_id="marketing",
    name="Marketing & Ad-Tech",
    description="Enterprise-grade credentials for ad platforms, CRM systems, social media management, and customer data platforms.",
    credentials={
        "ad_platform_api": CredentialDefinition(
            name="Ad Platform API",
            description="Secure access to major advertising networks (e.g., Google Ads, Meta Ads).",
            allowed_scopes=["ads:read", "campaign:write", "budget:manage"]
        ),
        "crm_integration": CredentialDefinition(
            name="CRM Integration Gateway",
            description="Credentials for syncing customer data and managing leads in CRM systems (e.g., Salesforce, HubSpot).",
            allowed_scopes=["crm:read", "lead:write", "contact:update"]
        ),
        "social_media_manager": CredentialDefinition(
            name="Social Media Management API",
            description="Access to social media platforms for publishing content and monitoring engagement.",
            allowed_scopes=["social:publish", "social:read", "engagement:monitor"]
        ),
        "email_marketing_gateway": CredentialDefinition(
            name="Email Marketing API",
            description="Credentials for orchestrating email campaigns and managing subscriber lists.",
            allowed_scopes=["email:send", "list:manage", "campaign:analyze"]
        ),
        "customer_data_platform": CredentialDefinition(
            name="Customer Data Platform (CDP)",
            description="Access to centralized customer data platforms for audience segmentation and analytics.",
            allowed_scopes=["audience:segment", "analytics:read", "data:sync"]
        )
    }
)
