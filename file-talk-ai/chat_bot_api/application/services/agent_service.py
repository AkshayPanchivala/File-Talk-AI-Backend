"""
Agent Service
Base service for AI agent operations
"""
import os
from phi.agent import Agent
from phi.model.groq import Groq
from typing import Optional, List
from config.env_config import config
from chat_bot_api.domain.exceptions import (
    AgentInitializationError,
    AgentProcessingError,
    GroqAPIError
)
from .base_service import BaseService


class AgentService(BaseService):
    """Base service for AI agent operations"""

    def __init__(self):
        """Initialize agent service"""
        super().__init__()
        self._setup_groq_api()

    def _setup_groq_api(self):
        """Setup Groq API key"""
        os.environ["GROQ_API_KEY"] = config.GROQ_API_KEY

    def create_agent(
        self,
        name: str,
        description: str,
        role: str,
        instructions: List[str],
        model_id: Optional[str] = None,
        markdown: bool = True,
        fallback_messages: Optional[List[str]] = None,
        knowledge_base = None
    ) -> Agent:
        """
        Create AI agent

        Args:
            name: Agent name
            description: Agent description
            role: Agent role
            instructions: List of instructions
            model_id: Model ID (defaults to config value)
            markdown: Enable markdown output
            fallback_messages: Fallback messages
            knowledge_base: IGNORED - Groq does not support knowledge_base tools

        Returns:
            Agent: Initialized agent

        Raises:
            AgentInitializationError: If agent creation fails
        """
        try:
            self.log_info(f"Creating agent: {name}")

            model_id = model_id or config.GROQ_MODEL_ID

            # WARNING: Do NOT pass knowledge_base to Agent() when using Groq
            # Groq models don't support the search_knowledge_base function calling
            # Instead, manually query the knowledge base and pass context in the prompt
            agent = Agent(
                name=name,
                description=description,
                role=role,
                instructions=instructions,
                model=Groq(id=model_id),
                markdown=markdown,
                fallback_messages=fallback_messages or []
                # DO NOT add: knowledge_base=knowledge_base
            )

            self.log_info(f"Agent created successfully: {name}")
            return agent

        except Exception as e:
            self.log_error(f"Failed to create agent: {str(e)}", error=str(e), agent_name=name)
            raise AgentInitializationError(
                f"Failed to create agent {name}: {str(e)}",
                agent_name=name
            )

    def run_agent(self, agent: Agent, prompt: str) -> str:
        """
        Run agent with prompt

        Args:
            agent: Agent instance
            prompt: Input prompt

        Returns:
            str: Agent response

        Raises:
            AgentProcessingError: If processing fails
            GroqAPIError: If API call fails
        """
        try:
            self.log_info(f"Running agent: {agent.name}")

            response = agent.run(prompt)

            # Extract content from response
            if isinstance(response, dict):
                content = response.get("content", "").strip()
            else:
                content = getattr(response, "content", "").strip()

            if not content:
                raise AgentProcessingError("Empty response from agent", agent_name=agent.name)

            self.log_info(f"Agent processing completed: {agent.name}")
            return content

        except Exception as e:
            error_msg = str(e).lower()

            # Check for API-specific errors
            if 'api' in error_msg or 'groq' in error_msg or 'rate' in error_msg:
                self.log_error(f"Groq API error: {str(e)}", error=str(e))
                raise GroqAPIError(f"Groq API error: {str(e)}", api_response=str(e))

            self.log_error(f"Agent processing error: {str(e)}", error=str(e), agent_name=agent.name)
            raise AgentProcessingError(
                f"Agent processing failed: {str(e)}",
                agent_name=agent.name
            )
