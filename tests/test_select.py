from law_n_nsql_engine.engine import execute_query
from law_n_nsql_engine.adapters.in_memory_adapter import InMemoryNetworkAdapter


def test_basic_select_routes():
    adapter = InMemoryNetworkAdapter()
    query = """
    SELECT tower_id, frequency, latency
    FROM network.routes
    WHERE device_from = "0xA4C1"
    AND signal_quality > 0.85;
    """
    result = execute_query(query, adapter)
    assert len(result) == 1
    row = result[0]
    assert "tower_id" in row
    assert "frequency" in row
    assert "latency" in row
