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

    def _init_service(self):
        self._baseUrl = "https://chat." + self._PRODUCTION_DOMAIN

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
                    "channelNumber": And(
                        str,
                        lambda s: validate_phone(s),
                        error=f"Invalid channel number: {channel_number}",
                    ),
                    "channel": And(
                        str,
                        lambda s: s in chatTypes,
                        error=f"Invalid channel type, valid types are {list(chatTypes.keys())}",
                    ),
                    "customerNumber": And(
                        str,
                        lambda s: validate_phone(s),
                        error=f"Invalid customer number: {customer_number}",
                    ),
                    "body": {
                        "type": And(
                            str,
                            lambda s: s in messageTypes,
                            error=f"Invalid message type, valid types are {list(messageTypes.keys())}",
                        ),
                        Optional("latitude"): And(float, len),
                        Optional("longitude"): And(float, len),
                        Optional("media"): And(
                            str,
                            lambda s: s in mediaTypes,
                            error=f"Invalid media type, valid types are {list(mediaTypes.keys())}",
                        ),
                        Optional("url"): And(str, len),
                        Optional("text"): And(str, len),
                    },
                }
            )
            data = messageSchema.validate(data)
        except SchemaError as err:
            raise ValueError(err)

        url = self._make_url("/message/send")
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
        data = json.dumps(data)

        return self._make_request(
            url,
            "POST",
            headers=headers,
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
        headers = dict(self._headers)
        headers["Content-Type"] = "application/json"
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
