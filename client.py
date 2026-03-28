from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()


async def main():

    client = MultiServerMCPClient(
        {
            "ServerA": {
                "transport": "http",
                "url": "http://localhost:8000/mcp",
            }
        }
    )
    tools = await client.get_tools()

    gpt5nano = ChatOpenAI(model="gpt-5-nano")
    agent = create_agent(
        model=gpt5nano,
        tools=tools,
    )

    response = await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": "I'm going to Paris tomorrow. What's the weather in the next 24 hours and what should I pack?"}]}
    )

    messages = response["messages"]
    print("\n Final Text:")
    last_ai = next(m for m in reversed(messages)
                   if getattr(m, "type", None) == "ai")
    final_text = last_ai.text
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())
