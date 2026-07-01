import time


def trace_start(state, node):

    state["trace"].append(
        {
            "node": node,
            "start": time.time(),
            "end": None,
            "duration": None,
            "status": "running",
            "error": None,
        }
    )


def trace_end(
    state,
    status="success",
    error=None,
):

    item = state["trace"][-1]

    item["end"] = time.time()

    item["duration"] = round(
        item["end"] - item["start"],
        3
    )

    item["status"] = status

    item["error"] = error
