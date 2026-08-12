import json
import traceback
from threading import Thread

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.graph.workflow import graph
from app.graph.workflow import ChatRequest

from app.core.events import (
    subscribe,
    unsubscribe,
    publish,
)


router = APIRouter(
    prefix="/chat",
    tags=["Streaming Chat"],
)


@router.post("/stream")
async def stream_chat(request: ChatRequest):

    queue = subscribe()

    print("=" * 80)
    print("NEW STREAM SUBSCRIBER")
    print(f"SESSION ID: {request.session_id}")
    print(f"QUERY: {request.query}")
    print("=" * 80)

    def run_workflow():

        print("=" * 80)
        print("THREAD STARTED")
        print("=" * 80)

        try:

            print("BEFORE GRAPH")

            result = graph.invoke(
                {
                    "query": request.query,
                    "session_id": request.session_id,
                }
            )

            print("=" * 80)
            print("GRAPH FINISHED")
            print(result)
            print("=" * 80)

            # If the workflow itself did not publish
            # the final answer, publish it here.
            answer = ""

            if isinstance(result, dict):
                answer = result.get("answer", "") or ""

            if answer:
                publish(
                    "final_answer",
                    "Final answer generated",
                    {
                        "answer": answer,
                    },
                )

            # This is the ONLY event that closes
            # the frontend SSE stream.
            publish(
                "stream_finished",
                "Stream completed",
            )

        except Exception as exc:

            print("=" * 80)
            print("WORKFLOW CRASHED")
            print("=" * 80)

            traceback.print_exc()

            publish(
                "stream_error",
                str(exc),
            )

            publish(
                "stream_finished",
                "Stream completed with error",
            )

    Thread(
        target=run_workflow,
        daemon=True,
    ).start()

    def event_generator():

        try:

            while True:

                event = queue.get()

                event_type = event.get("type")

                print(
                    f"SENDING: {event_type}"
                )

                yield (
                    f"event: {event_type}\n"
                    f"data: {json.dumps(event)}\n\n"
                )

                if event_type == "stream_finished":

                    print("STREAM FINISHED")

                    break

        except GeneratorExit:

            print("CLIENT DISCONNECTED")

        except Exception:

            print("STREAM GENERATOR ERROR")

            traceback.print_exc()

        finally:

            unsubscribe(queue)

            print(
                "STREAM CLEANUP COMPLETE"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )