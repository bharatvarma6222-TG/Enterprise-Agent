import json
import uuid

from pathlib import Path
from datetime import datetime


TRACE_DIRECTORY = Path("data/traces")

TRACE_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


def save_trace(trace: dict):

    trace_id = str(uuid.uuid4())

    trace["trace_id"] = trace_id

    trace["created_at"] = datetime.now().isoformat()

    file_path = TRACE_DIRECTORY / f"{trace_id}.json"

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            trace,
            f,
            indent=4,
            ensure_ascii=False,
        )

    return trace_id


def get_trace(trace_id: str):

    file_path = TRACE_DIRECTORY / f"{trace_id}.json"

    if not file_path.exists():
        return None

    with open(
        file_path,
        encoding="utf-8",
    ) as f:

        return json.load(f)


def get_latest_trace():

    files = sorted(
        TRACE_DIRECTORY.glob("*.json"),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    if not files:
        return None

    with open(
        files[0],
        encoding="utf-8",
    ) as f:

        return json.load(f)


def get_all_traces():

    traces = []

    files = sorted(
        TRACE_DIRECTORY.glob("*.json"),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    for file in files:

        with open(
            file,
            encoding="utf-8",
        ) as f:

            traces.append(
                json.load(f)
            )

    return traces
