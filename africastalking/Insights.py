import json
from .Service import Service, validate_phone


class InsightService(Service):
    def __init__(self, username, api_key):
        super(InsightService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = "https://insights."
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN + "/v1"
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN + "/v1"

    def check_sim_swap_state(self, phone_numbers, callback=None):
        url = self._make_url("/sim-swap")
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
        for phone_number in phone_numbers:
            if not validate_phone(phone_number):
                raise ValueError(
                    "Invalid phone number in list of phone numbers: %s", phone_number
                )
        data = {
            "username": self._username,
            "phoneNumbers": phone_numbers,
        }
        data = json.dumps(data)
        return self._make_request(
            url, "POST", headers=headers, params=None, data=data, callback=callback
        )
