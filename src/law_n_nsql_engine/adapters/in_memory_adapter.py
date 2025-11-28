from abc import ABC, abstractmethod
from typing import List, Dict, Any

from . import mock_data


class BaseNetworkAdapter(ABC):
    @abstractmethod
    def fetch_table(self, table: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def fetch_routes_between(self, device_from: str, device_to: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def inspect_frequency(self, frequency: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def inspect_device(self, device_id: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def inspect_tower(self, tower_id: str) -> Dict[str, Any]:
        ...


class InMemoryNetworkAdapter(BaseNetworkAdapter):
    """
    Simple in-memory mock adapter backed by mock_data.
    """

    def __init__(self):
        self._devices = mock_data.DEVICES
        self._towers = mock_data.TOWERS
        self._routes = mock_data.ROUTES
        self._frequencies = mock_data.FREQUENCIES

    def fetch_table(self, table: str) -> List[Dict[str, Any]]:
        table = table.strip()
        if table == "network.devices":
            return self._devices
        if table == "network.towers":
            return self._towers
        if table == "network.routes":
            return self._routes
        if table == "network.frequencies":
            return self._frequencies
        raise ValueError(f"Unknown table: {table}")

    def fetch_routes_between(self, device_from: str, device_to: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._routes
            if r.get("device_from") == device_from and r.get("device_to") == device_to
        ]

    def inspect_frequency(self, frequency: str) -> Dict[str, Any]:
        freq = next((f for f in self._frequencies if f.get("name") == frequency), None)
        if not freq:
            return {"status": "not_found", "frequency": frequency}
        return {"status": "ok", "frequency": freq}

    def inspect_device(self, device_id: str) -> Dict[str, Any]:
        dev = next((d for d in self._devices if d.get("deviceId") == device_id), None)
        if not dev:
            return {"status": "not_found", "deviceId": device_id}
        return {"status": "ok", "device": dev}

    def inspect_tower(self, tower_id: str) -> Dict[str, Any]:
        tower = next((t for t in self._towers if t.get("towerId") == tower_id), None)
        if not tower:
            return {"status": "not_found", "towerId": tower_id}
        return {"status": "ok", "tower": tower}
