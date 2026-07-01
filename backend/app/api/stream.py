import json
from threading import Thread

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.graph.workflow import graph
from app.graph.workflow import ChatRequest

from app.core.events import (
    subscribe,
    unsubscribe,
)

router = APIRouter(
    prefix="/chat",
    tags=["Streaming Chat"]
)


@router.post("/stream")
async def stream_chat(request: ChatRequest):

    queue = subscribe()

    def run_workflow():

        graph.invoke(
            {
                "query": request.query,
                "session_id": request.session_id
            }
        )

    Thread(
        target=run_workflow,
        daemon=True
    ).start()

    def event_generator():

        try:

            while True:

                event = queue.get()
                print("SENDING:", event["type"])

                yield (
                    f"event: {event['type']}\n"
                    f"data: {json.dumps(event)}\n\n"
                )

                if event["type"] == "memory_saved":
                    break

        finally:

            unsubscribe(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
