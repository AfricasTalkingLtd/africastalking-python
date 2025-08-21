"""
Application

fetchApplicationData(): Fetch app info i.e. balance.
"""

import africastalking
import unittest
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Application


class TestApplicationService(unittest.TestCase):
    @responses.activate
    def test_fetch_account(self):
        responses.add(
            responses.GET,
            f"https://api.africastalking.com/version1/user?username={USERNAME}",
            json={"userData": {"balance": "KES 1785.50"}},
            status=200,
        )
        res = service.fetch_application_data()
        assert res["userData"]["balance"] is not None


if __name__ == "__main__":
    unittest.main()
