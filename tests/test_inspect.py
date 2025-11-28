from law_n_nsql_engine.engine import execute_query
from law_n_nsql_engine.adapters.in_memory_adapter import InMemoryNetworkAdapter


def test_inspect_frequency():
    adapter = InMemoryNetworkAdapter()
    query = 'INSPECT FREQUENCY 3.42GHz;'
    result = execute_query(query, adapter)[0]
    assert result["status"] == "ok"
    assert result["frequency"]["name"] == "3.42GHz"
