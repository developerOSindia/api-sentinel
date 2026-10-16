"""
Unit tests for api-sentinel business logic.
"""

import sys
import unittest
from pathlib import Path

# Ensure app root is in sys.path
APP_ROOT = Path(__file__).resolve().parent.parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.sentinel_core import MockRouteRegistry


class TestSentinel(unittest.TestCase):
    def test_mock_registry(self):
        registry = MockRouteRegistry()
        registry.add_route("/v1/users", "GET", 200, {"users": ["alice", "bob"]})

        # Match check
        res = registry.simulate_request("/v1/users", "GET")
        self.assertTrue(res["matched"])
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(len(res["body"]["users"]), 2)

        # 404 check
        res_404 = registry.simulate_request("/v1/unknown", "GET")
        self.assertFalse(res_404["matched"])
        self.assertEqual(res_404["status_code"], 404)


if __name__ == "__main__":
    unittest.main()
