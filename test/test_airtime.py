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
        currency_code = "KES"
        amount = str(random.randint(10, 1000))
        phone = '+254718763456' 
        res = service.send(phone_number=phone, amount=amount, currency_code=currency_code)
        assert res['numSent'] == 1

    def test_send_multiple(self):
        res = service.send(recipients=[
            {'phoneNumber': '+2348160663047', 'amount': str(random.randint(1, 10)), 'currency_code': 'USD'},
            {'phoneNumber': '+254718769881', 'amount':str(random.randint(138, 13223)), 'currency_code':  'KES'},
        ])
        assert res['numSent'] == 2

    def test_missing_parameter_send_failure(self):

        def missing_amount():
            service.send(recipients=[
                {'phoneNumber': '+254718769881', 'currency_code': 'KES'}
            ])
        def missing_phoneNumber():
            service.send(recipients=[
                {'amount':str(random.randint(138, 13223)), 'currency_code': 'KES'}
            ])
        def missing_currencyCode():    
            service.send(recipients=[
                {'phoneNumber': '+254718769881', 'amount':str(random.randint(138, 13223))}
            ])    

        self.assertRaises(ValueError, missing_amount)
        self.assertRaises(ValueError, missing_phoneNumber)
        self.assertRaises(ValueError, missing_currencyCode)    

if __name__ == '__main__':
    unittest.main()
