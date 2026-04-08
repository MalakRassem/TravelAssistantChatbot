from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils.task import new_task
from a2a.types import (
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)
from a2a.utils.message import new_agent_text_message
from a2a.utils.artifact import new_text_artifact


class ChatbotAgentExecutor(AgentExecutor):

    def __init__(self, agent) -> None:
        self.agent = agent

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_input = context.get_user_input()
        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=TaskState.working,  # V0.3 vs V1.0 diff TaskState.TASK_STATE_WORKING
                    message=new_agent_text_message('Processing request...'),
                ),
                final=False,
            )
        )

        result = await self.agent.invoke(user_input)

        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                artifact=new_text_artifact(name='result', text=result),
            )
        )
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                # V0.3 vs V1.0 diff TaskState.TASK_STATE_COMPLETED
                status=TaskStatus(state=TaskState.completed),
                final=True
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")
