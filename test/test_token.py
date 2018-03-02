"""
Token

createCheckoutToken(phoneNumber: String): Create a new checkout token for phoneNumber

generateAuthToken(): Generate an auth token to us for authentication instead of the API key.

"""
import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Token


class TestTokenService(unittest.TestCase):

    def test_create_checkout_token(self):
        res = service.create_checkout_token("+254718769882")
        assert res['token'] != "None"

    def test_generate_auth_token(self):
        res = service.generate_auth_token()
        assert res['lifetimeInSeconds'] == 3600


if __name__ == '__main__':
    unittest.main()
