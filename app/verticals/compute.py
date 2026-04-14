from app.verticals.base import CredentialPack, CredentialDefinition

ComputeCredentialPack = CredentialPack(
    pack_id="compute",
    name="Compute & AI",
    description="Core credentials for AI model inference and cloud compute resources.",
    credentials={
        "openai_api": CredentialDefinition(
            name="OpenAI API Key",
            description="Access to OpenAI language models.",
            allowed_scopes=["model:read", "model:execute", "fine_tune:write"]
        ),
        "anthropic_api": CredentialDefinition(
            name="Anthropic API Key",
            description="Access to Anthropic Claude models.",
            allowed_scopes=["model:read", "model:execute"]
        ),
        "aws_compute": CredentialDefinition(
            name="AWS Compute Access",
            description="AWS EC2 and Lambda compute access.",
            allowed_scopes=["ec2:manage", "lambda:invoke"]
        ),
        "gpu_cluster": CredentialDefinition(
            name="GPU Cluster Access",
            description="Access to dedicated GPU clusters for training/inference.",
            allowed_scopes=["gpu:allocate", "job:submit"]
        )
    }
)
