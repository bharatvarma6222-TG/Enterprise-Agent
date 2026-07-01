import time


def llm_start():

    return time.time()


def llm_end(
    state,
    node,
    model,
    start_time,
    prompt_tokens=None,
    completion_tokens=None,
):

    latency = round(
        time.time() - start_time,
        3
    )

    total = None

    if (
        prompt_tokens is not None
        and completion_tokens is not None
    ):
        total = (
            prompt_tokens
            + completion_tokens
        )

    state["llm_metrics"].append(
        {
            "node": node,
            "model": model,
            "latency": latency,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total,
        }
    )
