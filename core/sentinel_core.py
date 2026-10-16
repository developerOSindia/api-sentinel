"""
Core business logic for API Sentinel flagship application.
Zero Streamlit or UI dependencies.
"""

from typing import Dict, Any, List


class MockRouteRegistry:
    """In-memory mock endpoint manager for developer API simulation."""

    def __init__(self):
        self._routes: Dict[str, Dict[str, Any]] = {}

    def add_route(self, path: str, method: str, status_code: int, response_body: Dict[str, Any]):
        key = f"{method.upper()}:{path}"
        self._routes[key] = {
            "path": path,
            "method": method.upper(),
            "status_code": status_code,
            "response_body": response_body,
        }

    def simulate_request(self, path: str, method: str) -> Dict[str, Any]:
        key = f"{method.upper()}:{path}"
        if key in self._routes:
            route = self._routes[key]
            return {
                "matched": True,
                "status_code": route["status_code"],
                "body": route["response_body"],
            }
        return {
            "matched": False,
            "status_code": 404,
            "body": {"error": "Route not registered in Sentinel mock registry"},
        }

    def list_routes(self) -> List[Dict[str, Any]]:
        return list(self._routes.values())
