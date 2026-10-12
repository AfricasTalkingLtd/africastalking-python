from .Service import DEFAULT_TIMEOUT_S, Service, validate_phone
from schema import And, Optional, Schema


class VoiceService(Service):
    def __init__(self, username, api_key):
        super(VoiceService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = "https://voice."
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN

    def call(self, callFrom, callTo, callback=None, timeout=DEFAULT_TIMEOUT_S):
        for phone_number in callTo:
            if not validate_phone(phone_number):
                raise ValueError("Invalid callTo phone number:" + phone_number)

        callTo = ",".join(callTo)
        url = self._make_url("/call")
        data = {
            "username": self._username,
            "from": callFrom,
            "to": callTo,
        }
        headers = dict(self._headers)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self._make_request(
            url,
            "POST",
            headers,
            params=None,
            data=data,
            callback=callback,
            timeout=timeout,
        )

    def fetch_queued_calls(
        self, phone_number, callback=None, timeout=DEFAULT_TIMEOUT_S
    ):
        if not validate_phone(phone_number):
            raise ValueError("Invalid phone number")

        url = self._make_url("/queueStatus")
        data = {
            "username": self._username,
            "phoneNumbers": phone_number,
        }
        return self._make_request(
            url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
            timeout=timeout,
        )

    def media_upload(self, phone_number, url, callback=None, timeout=DEFAULT_TIMEOUT_S):
        if not validate_phone(phone_number):
            raise ValueError("Invalid phone number")

        call_url = self._make_url("/mediaUpload")
        data = {
            "username": self._username,
            "phoneNumber": phone_number,
            "url": url,
        }
        return self._make_request(
            call_url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
            timeout=timeout,
        )

    def request_compatibility_token(
        self,
        client_name,
        phone_number,
        incoming=True,
        outgoing=True,
        expire=86400,
        callback=None,
        timeout=DEFAULT_TIMEOUT_S,
    ):
        tokenSchema = Schema(
            {
                "username": And(str),
                "phoneNumber": And(
                    str,
                    lambda s: validate_phone(s),
                    error=f"Invalid phone number: {phone_number}",
                ),
                "clientName": And(str),
                "incoming": And(bool),
                "outgoing": And(bool),
                "expire": And(lambda f: float(f) > 0),
            }
        )
        data = {
            "username": self._username,
            "phoneNumber": phone_number,
            "clientName": client_name,
            "incoming": incoming,
            "outgoing": outgoing,
            "expire": expire,
        }
        data = tokenSchema.validate(data)
        url = "https://webrtc.africastalking.com/capability-token/request"
        return self._make_request(
            url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
            timeout=timeout,
        )
