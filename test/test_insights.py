"""
Insights

fetchApplicationData(): Fetch app info i.e. balance.
"""

import africastalking
import unittest
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Insights


class TestInsightsService(unittest.TestCase):
    @responses.activate
    def test_sim_swap_state(self):
        responses.add(
            responses.POST,
            "https://insights.africastalking.com/v1/sim-swap",
            json={
                "transactionId": "a4f740c9-b0e4-4e89-a55d-8244d77383d2",
                "status": "Processed",
                "totalCost": {
                    "amount": 1,
                    "currencyCode": "KES",
                },
                "responses": [
                    {
                        "phoneNumber": {
                            "carrierName": "Safaricom",
                            "countryCode": 254,
                            "networkCode": "Safaricom",
                            "number": "+2547xxxxxxxx",
                            "numberType": "Mobile",
                        },
                        "status": "Queued",
                        "requestId": "ATSwpid_e6968e1d3a8e95ffa3dd9454dde5d1ab",
                        "cost": {"amount": 1, "currencyCode": "KES"},
                    }
                ],
            },
            status=200,
        )
        res = service.check_sim_swap_state(["+254712345678"])
        assert res["status"] == "Processed"


if __name__ == "__main__":
    unittest.main()
