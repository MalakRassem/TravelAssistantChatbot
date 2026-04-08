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
from agent import build_action_agent

if __name__ == '__main__':
    geocode_skill = AgentSkill(
        id='Geocode',
        name='Returns geocode of a place',
        description='returns latitude and longitude of a location',
        tags=['geocode', 'latitude and longitude'],
        examples=['what is the geocode of Graz?',
                  'lat and lon of Paris, France'],
    )
    forecast_skill = AgentSkill(
        id='forecast',
        name='Returns a weather forecast for a place',
        description='Returns a weather forecast for a place',
        tags=['forecast', 'weather'],
        examples=['what is the weather like in Graz right now?',
                  'temperature in Paris over the next 24 hours'],
    )

    public_agent_card = AgentCard(
        name='Action Agent',
        description='An agent that can output a weather forecast or a geocode for a place',
        url='http://localhost:9999/',  # V diff
        preferredTransport='JSONRPC',  # V diff
        icon_url='http://localhost:9999/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(
            streaming=True,
        ),
        supported_interfaces=[
            AgentInterface(
                transport='JSONRPC',
                url='http://localhost:9999',
            )
        ],
        skills=[geocode_skill, forecast_skill],
    )

    action_agent = asyncio.run(build_action_agent())

    request_handler = DefaultRequestHandler(
        agent_executor=ChatbotAgentExecutor(action_agent),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='127.0.0.1', port=9999)
