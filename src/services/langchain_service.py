from langchain.agents import create_agent
import logging
from typing import Optional, Any
from src.config.settings import settings
import os
from .rate_limiter import rate_limiter

logger = logging.getLogger(__name__)


class LangChainService:
    def __init__(self):
        logger.info("Initializing LangChain Service")
        self.api_key = settings.DEEPSEEK_API_KEY
        os.environ["DEEPSEEK_API_KEY"] = settings.DEEPSEEK_API_KEY
        self.agent = create_agent(
            model="deepseek-chat",  # intalled model="claude-sonnet-4-5-20250929",
            tools=[get_weather],
        )

    async def initialize(self):
        await rate_limiter.init_redis()

    def invoke(self, input_data: dict) -> Any:
        """Invoke the LangChain agent with input data."""
        return self.agent.invoke(
            {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
        )

    # return self.agent.invoke(input_data)


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# Run the agent

langchain_service = LangChainService()
