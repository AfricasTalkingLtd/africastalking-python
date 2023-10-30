import json
from schema import Schema, And, Optional
from .Service import (
    Service,
    validate_phone,
    validate_data_units,
    validate_data_validity,
)


class MobileDataService(Service):
    def __init__(self, username, api_key):
        super(MobileDataService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = "https://bundles."
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN

    def send(self, product_name, recipients, callback=None):
        schema = Schema(
            [
                {
                    "phoneNumber": And(str, lambda s: validate_phone(s)),
                    "quantity": And(lambda f: float(f) > 0),
                    "unit": And(str, lambda s: validate_data_units(s)),
                    "validity": And(str, lambda s: validate_data_validity(s)),
                    Optional("isPromoBundle"): And(bool),
                    Optional("metadata"): And(dict),
                }
            ]
        )
        recipients = schema.validate(recipients)
        url = self._make_url("/mobile/data/request")
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
        data = {
            "username": self._username,
            "productName": product_name,
            "recipients": recipients,
        }
        data = json.dumps(data)
        return self._make_request(
            url, "POST", headers=headers, params=None, data=data, callback=callback
        )
