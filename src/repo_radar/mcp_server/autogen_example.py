from autogen_ext.tools.mcp import StreamableHttpServerParams, mcp_server_tools
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
import asyncio


async def main():
    # 1. Define HTTP server parameters for MCP server
    server_params = StreamableHttpServerParams(
        url="http://127.0.0.1:8000/mcp/",  # URL of your MCP endpoint
        timeout=30.0,
        sse_read_timeout=300.0,
        terminate_on_close=True,
    )

    # 2. Automatically fetch all tools from the MCP server
    tools = await mcp_server_tools(server_params)

    # 3. Create your assistant agent with AutoGen
    assistant = AssistantAgent(
        name="assistant",
        model_client=OpenAIChatCompletionClient(model="gpt-3.5-turbo"),  # or gpt-4o
        tools=tools,
        reflect_on_tool_use=True,
    )

    # 4. Create user proxy for interactive inputs
    user = UserProxyAgent(name="you")

    # 5. Set up a conversation loop with exit command support
    team = RoundRobinGroupChat(
        participants=[user, assistant],
        termination_condition=TextMentionTermination("exit"),
    )

    stream = team.run_stream(task="Hello! What would you like to do? ")
    await Console(stream)
    # 6. Launch interactive console
    # await Console(team)


if __name__ == "__main__":
    asyncio.run(main())
