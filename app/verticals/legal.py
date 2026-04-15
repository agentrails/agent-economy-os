from app.verticals.base import CredentialPack, CredentialDefinition

LegalCredentialPack = CredentialPack(
    pack_id="legal",
    name="Legal & Compliance",
    description="Enterprise-grade credentials for legal contracts, IP registries, court filings, and e-signatures.",
    credentials={
        "legal_contract_access": CredentialDefinition(
            name="Legal Contract Access",
            description="Access to centralized legal contract repositories and lifecycle management systems.",
            allowed_scopes=["contract:read", "contract:write", "contract:draft"]
        ),
        "intellectual_property_registry": CredentialDefinition(
            name="Intellectual Property Registry",
            description="Credentials for querying and filing patents, trademarks, and copyrights.",
            allowed_scopes=["ip:search", "ip:file", "ip:manage"]
        ),
        "court_filing_api": CredentialDefinition(
            name="Court Filing API",
            description="Secure access to electronic court filing (e-filing) systems and docket retrieval.",
            allowed_scopes=["court:file", "docket:read", "case:track"]
        ),
        "ndaa_compliance": CredentialDefinition(
            name="NDAA Compliance Check",
            description="Access to supply chain and vendor compliance verification APIs (e.g., NDAA Section 889).",
            allowed_scopes=["vendor:verify", "supply_chain:audit"]
        ),
        "e_signature": CredentialDefinition(
            name="E-Signature Provider",
            description="Credentials for executing and verifying legally binding electronic signatures.",
            allowed_scopes=["signature:request", "signature:verify", "document:sign"]
        )
    }
)
