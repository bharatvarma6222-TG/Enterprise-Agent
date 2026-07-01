from dataclasses import dataclass
from typing import Optional


@dataclass
class NodeTrace:

    node: str

    start_time: float

    end_time: float

    duration: float

    status: str

    error: Optional[str] = None
