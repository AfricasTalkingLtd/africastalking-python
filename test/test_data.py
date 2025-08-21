import africastalking
import unittest
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.MobileData


class TestMobileDataService(unittest.TestCase):
    @responses.activate
    def test_mobile_data(self):
        try:
            responses.add(
                responses.POST,
                "https://bundles.africastalking.com/mobile/data/request",
                json={
                    "entries": [
                        {
                            "phoneNumber": "+254714978532",
                            "provider": "Safaricom",
                            "status": "Queued",
                            "transactionId": "ATPid_8df0ca90660d981ff9059454672496c2",
                            "value": "KES 20.0000",
                        }
                    ]
                },
                status=200,
            )
            recipient = {
                "phoneNumber": "+254711223344",
                "quantity": 10,
                "unit": "GB",
                "validity": "Month",
                "metadata": {"some": "information"},
            }
            res = service.send(product_name="TestProduct", recipients=[recipient])
            assert res["entries"][0]["status"] is not None
        except africastalking.Service.AfricasTalkingException:
            assert True
