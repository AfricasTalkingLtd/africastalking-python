"""
Token

generateAuthToken(): Generate an auth token to us for authentication instead of the API key.

"""

import africastalking
import unittest
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Token


class TestTokenService(unittest.TestCase):
    @responses.activate
    def test_generate_auth_token(self):
        responses.add(
            responses.POST,
            "https://api.africastalking.com/auth-token/generate",
            json={"lifetimeInSeconds": 3600, "token": "jriojrigj10939042904"},
            status=200,
        )
        res = service.generate_auth_token()
        assert res["lifetimeInSeconds"] == 3600


if __name__ == "__main__":
    unittest.main()
