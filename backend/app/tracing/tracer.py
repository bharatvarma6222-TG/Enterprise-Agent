import time
from datetime import datetime


def trace_start(state, node_name: str):

    if "trace" not in state:
        state["trace"] = []

    state["trace"].append(
        {
            "node": node_name,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "_start_time": time.perf_counter(),
        }
    )


def trace_end(
    state,
    status: str = "success",
    error: str | None = None,
):

    if "trace" not in state:
        return

    if not state["trace"]:
        return

    trace = state["trace"][-1]

    end = time.perf_counter()

    duration = round(
        end - trace["_start_time"],
        3,
    )

    trace["duration"] = duration

    trace["status"] = status

    trace["ended_at"] = datetime.now().isoformat()

    trace["error"] = error

    del trace["_start_time"]

    print(
        f"{trace['node']:<20}"
        f"{status:<12}"
        f"{duration} sec"
    )
