import uvicorn
import asyncio
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)

from agent_executor.executor import (
    ChatbotAgentExecutor,
)

from research_agent.agent import build_research_agent
if __name__ == '__main__':

    wiki_skill = AgentSkill(
        id='wikiextract',
        name='Returns a Wikipedia summary for a topic',
        description='Retrieves the introductory plain-text extract for a topic from Wikipedia',
        tags=['wikipedia', 'summary', 'encyclopedia', 'topic lookup'],
        examples=[
            'Give me a short Wikipedia summary of Rainbow Mountain',
            'What is Cusco?'
        ],
    )

    openalex_skill = AgentSkill(
        id='openalexsearchworks',
        name='Returns scholarly references for a query',
        description='Searches OpenAlex works and returns scholarly references relevant to a user question',
        tags=['openalex', 'scholarly references', 'papers', 'research'],
        examples=[
            'Find 2 scholarly references about altitude sickness prevention',
            'Search for papers about acute mountain sickness'
        ],
    )

    public_agent_card = AgentCard(
        name='Research Agent',
        description='An agent that can retrieve Wikipedia summaries and scholarly references from OpenAlex',
        url='http://localhost:9998/',  # V diff
        preferredTransport='JSONRPC',  # V diff
        icon_url='http://localhost:9998/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,
        ),
        supported_interfaces=[
            AgentInterface(
                transport='JSONRPC',
                url='http://localhost:9998',
            )
        ],
        skills=[wiki_skill, openalex_skill],
    )

    research_agent = asyncio.run(build_research_agent())

    request_handler = DefaultRequestHandler(
        agent_executor=ChatbotAgentExecutor(research_agent),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='127.0.0.1', port=9998)
