"""
Airtime

send(phoneNumber: String, amount: String): Send airtime to a phone number.

send(recipients: Map<String,String>): Send airtime to a bunch of phone numbers. The keys in the recipients map are phone
    numbers while the values are airtime amounts.
"""

import africastalking
import unittest
import random
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Airtime


class TestAirtimeService(unittest.TestCase):
    @responses.activate
    def test_send_single(self):
        responses.add(
            responses.POST,
            "https://api.africastalking.com/version1/airtime/send",
            json={
                "errorMessage": "None",
                "numSent": 1,
                "totalAmount": "KES 1000.0000",
                "totalDiscount": "KES 40.0000",
                "responses": [
                    {
                        "phoneNumber": "+254718763456",
                        "errorMessage": "None",
                        "amount": "KES 1000.0000",
                        "status": "Sent",
                        "requestId": "ATQid_1be914ac47845eef1a1dab5d89ec50ff",
                        "discount": "KES 40.0000",
                    }
                ],
            },
            status=200,
        )
        currency_code = "KES"
        amount = str(random.randint(10, 1000))
        phone = "+254718763456"
        idempotency_key = "req-1234"
        max_num_retry = 4
        res = service.send(
            phone_number=phone,
            amount=amount,
            currency_code=currency_code,
            idempotency_key=idempotency_key,
            max_num_retry=max_num_retry,
        )
        assert res["numSent"] == 1

    @responses.activate
    def test_send_multiple(self):
        responses.add(
            responses.POST,
            "https://api.africastalking.com/version1/airtime/send",
            json={
                "errorMessage": "None",
                "numSent": 2,
                "totalAmount": "KES 1000.0000",
                "totalDiscount": "KES 40.0000",
                "responses": [
                    {
                        "phoneNumber": "+2348160663047",
                        "errorMessage": "None",
                        "amount": "KES 1000.0000",
                        "status": "Sent",
                        "requestId": "ATQid_1be914ac47845eef1a1dab5d89ec50ff",
                        "discount": "KES 40.0000",
                    },
                    {
                        "phoneNumber": "+254718769881",
                        "errorMessage": "None",
                        "amount": "KES 1000.0000",
                        "status": "KES",
                        "requestId": "ATQid_1be914ac47845eef1a1dab5d89ec50ff",
                        "discount": "KES 40.0000",
                    },
                ],
            },
            status=200,
        )
        res = service.send(
            recipients=[
                {
                    "phoneNumber": "+2348160663047",
                    "amount": str(random.randint(1, 10)),
                    "currency_code": "USD",
                },
                {
                    "phoneNumber": "+254718769881",
                    "amount": str(random.randint(138, 13223)),
                    "currency_code": "KES",
                },
            ]
        )
        assert res["numSent"] == 2

    def test_missing_parameter_send_failure(self):
        def missing_amount():
            service.send(
                recipients=[{"phoneNumber": "+254718769881", "currency_code": "KES"}]
            )

        def missing_phoneNumber():
            service.send(
                recipients=[
                    {"amount": str(random.randint(138, 13223)), "currency_code": "KES"}
                ]
            )

        def missing_currencyCode():
            service.send(
                recipients=[
                    {
                        "phoneNumber": "+254718769881",
                        "amount": str(random.randint(138, 13223)),
                    }
                ]
            )

        self.assertRaises(ValueError, missing_amount)
        self.assertRaises(ValueError, missing_phoneNumber)
        self.assertRaises(ValueError, missing_currencyCode)


if __name__ == "__main__":
    unittest.main()
