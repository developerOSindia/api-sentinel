"""
Unit tests for API Sentinel mock route engine.
"""

import sys
import unittest
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.sentinel_core import MockRouteRegistry


class TestSentinel(unittest.TestCase):
    def setUp(self):
        self.registry = MockRouteRegistry()

    def test_add_and_simulate_route(self):
        self.registry.add_route("/api/v1/user", "GET", 200, {"id": 1, "username": "kalash"})
        res = self.registry.simulate_request("/api/v1/user", "GET")
        self.assertTrue(res["matched"])
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(res["body"]["username"], "kalash")

    def test_missing_route_returns_404(self):
        res = self.registry.simulate_request("/nonexistent", "GET")
        self.assertFalse(res["matched"])
        self.assertEqual(res["status_code"], 404)
        self.assertIn("not registered", res["body"]["error"])

    def test_path_normalization(self):
        # Adding without leading slash
        self.registry.add_route("health", "get", 200, {"status": "healthy"})
        # Querying with leading slash and query string
        res = self.registry.simulate_request("/health?source=monitoring", "GET")
        self.assertTrue(res["matched"])
        self.assertEqual(res["status_code"], 200)

    def test_method_case_insensitivity(self):
        self.registry.add_route("/posts", "post", 201, {"created": True})
        res = self.registry.simulate_request("/posts", "POST")
        self.assertTrue(res["matched"])
        self.assertEqual(res["status_code"], 201)

    def test_remove_and_clear_routes(self):
        self.registry.add_route("/temp", "GET", 200, {})
        self.assertEqual(len(self.registry.list_routes()), 1)
        removed = self.registry.remove_route("/temp", "GET")
        self.assertTrue(removed)
        self.assertEqual(len(self.registry.list_routes()), 0)

        self.registry.add_route("/r1", "GET", 200, {})
        self.registry.add_route("/r2", "GET", 200, {})
        self.assertEqual(len(self.registry.list_routes()), 2)
        self.registry.clear()
        self.assertEqual(len(self.registry.list_routes()), 0)


if __name__ == "__main__":
    unittest.main()
