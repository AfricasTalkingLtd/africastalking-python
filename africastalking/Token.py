import json

from .Service import APIService


class TokenService(APIService):
    def __init__(self, username, api_key):
        super(TokenService, self).__init__(username, api_key)

    def generate_auth_token(self, callback=None):
        url = self._make_url("/auth-token/generate")
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
        data = json.dumps({"username": self._username})

        return self._make_request(
            url, "POST", headers, params=None, data=data, callback=callback
        )

    def create_checkout_token(self, phone_number, callback=None):
        url = self._make_url("/checkout/token/create")
        headers = dict(self._headers)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {"phoneNumber": phone_number}

        return self._make_request(
            url, "POST", headers, params=None, data=data, callback=callback
        )
