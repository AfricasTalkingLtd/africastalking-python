import json
from schema import And, Optional, Schema
from .Service import (
    DEFAULT_TIMEOUT_S,
    Service,
    validate_data_units,
    validate_data_validity,
    validate_phone,
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

    def send(self, product_name, recipients, callback=None, timeout=DEFAULT_TIMEOUT_S):
        schema = Schema(
            [
                {
                    "phoneNumber": And(str, lambda s: validate_phone(s)),
                    "quantity": And(lambda f: float(f) > 0),
                    "unit": And(str, lambda s: validate_data_units(s)),
                    "validity": And(str, lambda s: validate_data_validity(s)),
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
            url,
            "POST",
            headers=headers,
            params=None,
            data=data,
            callback=callback,
            timeout=timeout,
        )

    def find_transaction(
        self, transaction_id, callback=None, timeout=DEFAULT_TIMEOUT_S
    ):
        url = self._make_url("/query/transaction/find")
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
        params = {
            "username": self._username,
            "transactionId": transaction_id,
        }
        return self._make_request(
            url,
            "GET",
            headers=headers,
            data=None,
            params=params,
            callback=callback,
            timeout=timeout,
        )

    def fetch_wallet_balance(self, callback=None, timeout=DEFAULT_TIMEOUT_S):
        url = self._make_url("/query/wallet/balance")
        params = {
            "username": self._username,
        }
        return self._make_request(
            url,
            "GET",
            data=None,
            headers=self._headers,
            params=params,
            callback=callback,
            timeout=timeout,
        )
