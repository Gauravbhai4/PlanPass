"""Permit Setu: Configuration loader.

Loads Azure OpenAI credentials from environment variables (.env file).
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Azure OpenAI + app settings."""

    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv(
        "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"
    )
    # Optional separate vision-capable deployment. If unset, the main
    # deployment is used (which is fine if it's gpt-4o or similar).
    AZURE_OPENAI_VISION_DEPLOYMENT_NAME: str = os.getenv(
        "AZURE_OPENAI_VISION_DEPLOYMENT_NAME", ""
    )
    AZURE_OPENAI_API_VERSION: str = os.getenv(
        "AZURE_OPENAI_API_VERSION", "2024-10-21"
    )

    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    @classmethod
    def validate(cls) -> None:
        """Raise if required Azure OpenAI vars are missing."""
        missing = []
        if not cls.AZURE_OPENAI_ENDPOINT or "YOUR_RESOURCE_NAME" in cls.AZURE_OPENAI_ENDPOINT:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not cls.AZURE_OPENAI_API_KEY or cls.AZURE_OPENAI_API_KEY == "your-api-key-here":
            missing.append("AZURE_OPENAI_API_KEY")
        if missing:
            raise ValueError(
                "Missing or unset environment variables: "
                + ", ".join(missing)
                + ". Copy .env.example to .env and fill in real values."
            )


settings = Settings()
