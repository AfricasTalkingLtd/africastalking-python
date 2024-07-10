"""
Insights

fetchApplicationData(): Fetch app info i.e. balance.
"""

import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Insights


class TestInsightsService(unittest.TestCase):
    def test_sim_swap_state(self):
        res = service.check_sim_swap_state(["+254712345678"])
        assert res["status"] == "Processed"


if __name__ == "__main__":
    unittest.main()
