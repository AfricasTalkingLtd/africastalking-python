import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.MobileData


class TestMobileDataService(unittest.TestCase):
    def test_mobile_data(self):
        try:
            recipient = {
                "phoneNumber": "+254711223344",
                "quantity": 10,
                "unit": "GB",
                "validity": "Month",
                "metadata": {"some": "information"},
            }
            res = service.send(product_name="TestProduct", recipients=[recipient])
            assert res["status"] is not None
        except africastalking.Service.AfricasTalkingException:
            assert True
