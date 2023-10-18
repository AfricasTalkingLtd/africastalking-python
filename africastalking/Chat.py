import json
import requests
import threading
from .Service import Service, validate_phone, AfricasTalkingException
from schema import Schema, And, Optional, SchemaError


chatTypes = {"Whatsapp": "WhatsApp", "Telegram": "Telegram"}

messageTypes = {"Text": "Text", "Media": "Media", "Location": "Location"}

mediaTypes = {
    "Image": "Image",
    "Audio": "Audio",
    "Video": "Video",
    "Sticker": "Sticker",
    "Voice": "Voice",
}


class ChatService(Service):
    def __init__(self, username, api_key):
        super(ChatService, self).__init__(username, api_key)
        self._headers = {
            "Accept": "application/json",
            "User-Agent": "africastalking-python/2.0.0",
            "ApiKey": self._api_key,
            "Content-Type": "application/json",
        }

    def _init_service(self):
        self._baseUrl = "https://chat." + self._PRODUCTION_DOMAIN

    @staticmethod
    def __make_get_request(url, headers, data, params, callback=None):
        res = requests.get(url=url, headers=headers, params=params, json=data)

        if callback is None or callback == {}:
            return res
        else:
            callback(res)

    @staticmethod
    def __make_post_request(url, headers, data, params, callback=None):
        res = requests.post(
            url=url,
            headers=headers,
            params=params,
            json=data,
        )
        if callback is None or callback == {}:
            return res
        else:
            callback(res)

    def _make_request(self, url, method, headers, data, params, callback=None):
        method = method.upper()
        if callback is None:

            if method == "GET":
                res = self.__make_get_request(
                    url=url,
                    headers=headers,
                    data=data,
                    params=params,
                )
            elif method == "POST":
                res = self.__make_post_request(
                    url=url,
                    headers=headers,
                    data=data,
                    params=params,
                )
            else:
                raise AfricasTalkingException("Unexpected HTTP method: " + method)

            if 200 <= res.status_code < 300:
                if res.headers.get("content-type") == "application/json":
                    return res.json()
                else:
                    return res.text
            else:
                raise AfricasTalkingException(res.text)
        elif not callable(callback):
            raise RuntimeError("callback has to be callable. e.g. a function")
        else:

            def cb(response):
                if 200 <= response.status_code < 300:
                    if response.headers.get("content-type") == "application/json":
                        callback(None, response.json())
                    else:
                        callback(None, response.text)
                else:
                    callback(AfricasTalkingException(response.text), None)

            if method == "GET":
                _target = self.__make_get_request
            elif method == "POST":
                _target = self.__make_post_request
            else:
                raise AfricasTalkingException("Unexpected HTTP method: " + method)

            thread = threading.Thread(
                target=_target, args=(url, headers, data, params, cb)
            )
            thread.start()
            return thread

    def send(
        self,
        message,
        product_id,
        channel_number,
        customer_number,
        channel,
        callback=None,
    ):
        try:
            data = {
                "username": self._username,
                "productId": product_id,
                "channelNumber": channel_number,
                "channel": channel,
                "customerNumber": customer_number,
                "body": message,
            }
            messageSchema = Schema(
                {
                    "productId": And(str, len),
                    "username": And(str, len),
                    "productId": And(str, len),
                    "channelNumber": And(str, lambda s: validate_phone(s)),
                    "channel": And(str, lambda s: s in chatTypes),
                    "customerNumber": And(str, lambda s: validate_phone(s)),
                    "body": {
                        "type": And(str, lambda s: s in messageTypes),
                        Optional("latitude"): And(float, len),
                        Optional("longitude"): And(float, len),
                        Optional("media"): And(str, lambda s: s in mediaTypes),
                        Optional("url"): And(str, len),
                        Optional("text"): And(str, len),
                    },
                }
            )
            data = messageSchema.validate(data)
        except SchemaError as err:
            raise ValueError("Invalid body: " + err)

        url = self._make_url("/message/send")
        print(url)
        print(self._headers)
        print(data)

        return self._make_request(
            url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
        )

    def consent_response(self, channel_number, customer_number, channel, opt_in):
        if channel == chatTypes["whatsapp"]:
            if not validate_phone(customer_number):
                raise ValueError("Invalid phone number: " + customer_number)

            if not validate_phone(channel_number):
                raise ValueError("Invalid channel number: " + channel_number)

        url = self._make_url("/chat/consent")
        data = {
            "username": self._username,
            "channelNumber": channel_number,
            "channel": channel,
            "customerNumber": customer_number,
            "action": "OptIn" if opt_in else "OptOut",
        }

        return self._make_request(
            url, "POST", headers=self._headers, params=None, data=data
        )

    def send_template(
        self, message, product_id, channel_number, customer_number, channel
    ):
        self.send(message, product_id, channel_number, customer_number, channel)
