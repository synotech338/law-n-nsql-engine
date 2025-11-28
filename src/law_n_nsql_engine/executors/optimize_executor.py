from typing import Dict, Any

from ..ast import OptimizeRouteQuery
from ..adapters.in_memory_adapter import BaseNetworkAdapter


def execute_optimize(query: OptimizeRouteQuery, adapter: BaseNetworkAdapter) -> Dict[str, Any]:
    """
    Naive optimization:
    - Find all routes between device_from and device_to
    - Apply simple scoring based on latency and signal_quality
    - Respect frequency_band preference if present
    """
    routes = adapter.fetch_routes_between(query.device_from, query.device_to)
    if not routes:
        return {"status": "no_route_found"}

    pref_band = query.preferences.get("frequency_band")

    scored = []
    for r in routes:
        score = 0.0

        latency = r.get("latency", 1000)
        signal_quality = r.get("signal_quality", 0.0)
        frequency_band = r.get("frequency_band")

        # basic scoring
        score -= latency
        score += signal_quality * 100

        if pref_band and frequency_band == pref_band:
            score += 50

        scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_route = scored[0]

    return {
        "status": "ok",
        "route": best_route,
        "score": best_score,
        "goal": query.goal,
        "preferences": query.preferences,
    }
