"""
Core business logic for API Sentinel flagship application.
Zero Streamlit or UI dependencies.
"""

from typing import Dict, Any, List


class MockRouteRegistry:
    """In-memory mock endpoint manager for developer API simulation."""

    def __init__(self):
        self._routes: Dict[str, Dict[str, Any]] = {}

    def _normalize_key(self, path: str, method: str) -> str:
        clean_path = (path or "").strip()
        if not clean_path.startswith("/"):
            clean_path = "/" + clean_path
        # Strip query parameters if present
        clean_path = clean_path.split("?")[0]
        return f"{method.strip().upper()}:{clean_path}"

    def add_route(self, path: str, method: str, status_code: int, response_body: Dict[str, Any]):
        key = self._normalize_key(path, method)
        clean_path = path.strip()
        if not clean_path.startswith("/"):
            clean_path = "/" + clean_path
        self._routes[key] = {
            "path": clean_path.split("?")[0],
            "method": method.strip().upper(),
            "status_code": status_code,
            "response_body": response_body,
        }

    def simulate_request(self, path: str, method: str) -> Dict[str, Any]:
        key = self._normalize_key(path, method)
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

    def remove_route(self, path: str, method: str) -> bool:
        key = self._normalize_key(path, method)
        if key in self._routes:
            del self._routes[key]
            return True
        return False

    def clear(self):
        self._routes.clear()

    def list_routes(self) -> List[Dict[str, Any]]:
        return list(self._routes.values())
