from fastapi import APIRouter

from app.tracing.trace_store import (
    get_trace,
    get_all_traces,
    get_latest_trace,
)

router = APIRouter()


@router.get("/")
def list_traces():

    return get_all_traces()


@router.get("/latest")
def latest_trace():

    return get_latest_trace()


@router.get("/{trace_id}")
def trace(trace_id: str):

    return get_trace(trace_id)
