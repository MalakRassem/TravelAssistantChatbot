import httpx
import logging
from uuid import uuid4
from a2a.client import A2ACardResolver
from a2a.client.client import ClientConfig
from a2a.client.client_factory import ClientFactory
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from a2a.types import (
    Message,
    Part,
    Role,
    # SendMessageRequest, V0.3 vs V1.0
    # MessageSendParams, V0.3 vs V1.0
)


async def main(user_input) -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:9999'

    async with httpx.AsyncClient(timeout=httpx.Timeout(None)) as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        try:
            logger.info(
                '\nAttempting to fetch public agent card from: %s%s',
                base_url,
                AGENT_CARD_WELL_KNOWN_PATH,
            )
            _public_card = (
                await resolver.get_agent_card()
            )  # Fetches from default public path
            logger.info('\nSuccessfully fetched public agent card:')
            logger.info(_public_card)

        except Exception as e:
            logger.exception('\nCritical error fetching public agent card.')
            raise RuntimeError(
                '\nFailed to fetch the public agent card. Cannot continue.'
            ) from e

        print('\n--- Non-Streaming Call ---')
        client_factory = ClientFactory(config=ClientConfig(
            streaming=False, httpx_client=httpx_client))
        client = client_factory.create(_public_card)
        logger.info('\nNon-streaming A2AClient initialized.')

        parts = [Part(text=user_input)]
        message = Message(
            role=Role.user,  # V0.3 vs V1.0 diff Role.ROLE_USER
            parts=parts,
            message_id=uuid4().hex,
        )
        # request = SendMessageRequest(
        #     id=str(uuid4()),
        #     params=MessageSendParams(message=message),
        # ) #Legacy
        # request = SendMessageRequest(message=message) V0.3 vs V1.0 diff
        response = client.send_message(message)
        async for chunk in response:
            print('Response:')
            task, _ = chunk
            print(task.artifacts[0].parts[0].root.text)

        await client.close()


if __name__ == "__main__":
    import asyncio
    # user_input = "I’m traveling to Cusco and considering a day trip to Rainbow Mountain. Give me the next 48h weather in Cusco and an altitude-sickness prevention checklist with 2 scholarly references."
    user_input = "Give me the next 48h weather in Paris France"
    asyncio.run(main(user_input))
