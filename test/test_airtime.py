"""
Airtime

send(phoneNumber: String, amount: String): Send airtime to a phone number.

send(recipients: Map<String,String>): Send airtime to a bunch of phone numbers. The keys in the recipients map are phone
    numbers while the values are airtime amounts.
"""
import africastalking
import unittest
import random
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Airtime


class TestAirtimeService(unittest.TestCase):

    def test_send_single(self):
        amount = "KES " + str(random.randint(10, 1000))
        phone = '+25471876' + str(random.randint(1000, 9999))
        res = service.send(phone_number=phone, amount=amount)
        assert res['numSent'] == 1

    def test_send_multiple(self):
        res = service.send(recipients=[
            {'phoneNumber': '+2348160663047', 'amount': 'USD ' + str(random.randint(1, 10))},
            {'phoneNumber': '+254718769881', 'amount': 'KES ' + str(random.randint(138, 13223))},
        ])
        assert res['numSent'] == 2


if __name__ == '__main__':
    unittest.main()
