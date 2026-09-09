import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class OpenAIHelper:
    """Small wrapper around the OpenAI API used by the analysis pipeline."""

    def __init__(self, api_key: str | None = None):
        """Initialize the client using an explicit key or OPENAI_API_KEY."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured. "
                "Set it in the environment or in the project's .env file."
            )

        self.client = OpenAI(api_key=self.api_key)

    def get_openai_response(
        self,
        system_role: str,
        user_input: str,
        model: str = "gpt-3.5-turbo",
    ) -> str:
        """Send a system/user prompt pair to the configured OpenAI model."""
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_input},
            ],
        )

        return response.choices[0].message.content or ""
