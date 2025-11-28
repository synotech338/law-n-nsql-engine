from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Condition:
    field: str
    op: str  # "=", "!=", "<", ">", "<=", ">=", "MATCHES"
    value: Any


@dataclass
class SelectQuery:
    fields: List[str]
    table: str
    conditions: List[Condition]


@dataclass
class OptimizeRouteQuery:
    device_from: str
    device_to: str
    preferences: Dict[str, Any]
    goal: Optional[Dict[str, str]]  # {"type": "MINIMIZE", "field": "latency"}


@dataclass
class InspectQuery:
    target_type: str  # "FREQUENCY" | "DEVICE" | "TOWER"
    value: Any
