from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class ActionAgent:
    def __init__(self, lc_agent):
        self.lc_agent = lc_agent

    async def invoke(self, user_input: str) -> str:
        print(f"Action Agent received: {user_input}")
        response = await self.lc_agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        messages = response["messages"]
        print(messages)
        print("\n Final Text:")
        last_ai = next(m for m in reversed(messages)
                       if getattr(m, "type", None) == "ai")
        final_text = last_ai.text
        print(final_text)
        return final_text


async def build_action_agent():

    client = MultiServerMCPClient(
        {
            "ServerA": {
                "transport": "http",
                "url": "http://localhost:8000/mcp",
            },
        }
    )
    tools = await client.get_tools()

    gpt5nano = ChatOpenAI(model="gpt-5-nano", temperature=0)
    lc_agent = create_agent(
        store=False,
        model=gpt5nano,
        system_prompt="Always use a tool when you can. Definition or explanations must be retrieved via a tool. Scholarly references must be retrieved via a tool. Weatherforecast must be retrieved via tools",
        tools=tools,
    )
    return ActionAgent(lc_agent)
