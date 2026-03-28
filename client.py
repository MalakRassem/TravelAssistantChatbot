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
            },
            "ServerB": {
                "transport": "http",
                "url": "http://localhost:8001/mcp",
            }
        }
    )
    tools = await client.get_tools()

    gpt5nano = ChatOpenAI(model="gpt-4.1", temperature=0)
    agent = create_agent(
        store=False,
        model=gpt5nano,
        system_prompt="Always use a tool when you can. Definition or explanations must be retrieved via a tool. Scholarly references must be retrieved via a tool. Weatherforecast must be retrieved via tools",
        tools=tools,
    )

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "I’m traveling to Cusco and considering a day trip to Rainbow Mountain. Give me the next 48h weather in Cusco and an altitude-sickness prevention checklist with 2 scholarly references."}]}

    )

    messages = response["messages"]
    print(messages)
    print("\n Final Text:")
    last_ai = next(m for m in reversed(messages)
                   if getattr(m, "type", None) == "ai")
    final_text = last_ai.text
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())
