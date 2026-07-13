"""Agent creation for the Keel multi-agent system.

Each agent is a Semantic Kernel ChatCompletionAgent backed by Claude via the
AnthropicChatCompletion connector.
"""

import os
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion


def build_agent(agent_name, instructions, model_id=None, plugins=None):
    """Creates a Claude-backed agent."""
    model_id = model_id or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    service = AnthropicChatCompletion(
        ai_model_id=model_id,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        service_id=agent_name,
    )
    return ChatCompletionAgent(
        service=service,
        name=agent_name,
        instructions=instructions,
        plugins=plugins or [],
    )


async def create_or_reuse_agent(client=None, agent_name=None, model_deployment_name=None,
                                instructions=None, plugins=None, connections=None):
    """Creates an agent for the given definition.

    Web search is provided to the risk agents via WebSearchPlugin.
    """
    print(f"Creating Claude-backed agent: {agent_name}")
    return build_agent(
        agent_name=agent_name,
        instructions=instructions,
        model_id=model_deployment_name,
        plugins=plugins,
    )
