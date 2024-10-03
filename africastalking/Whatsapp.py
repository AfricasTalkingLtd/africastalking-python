import json
from .Service import Service, validate_phone, AfricasTalkingException
from schema import Schema, And, Optional, SchemaError


mediaTypes = {
    "Image": "Image",
    "Audio": "Audio",
    "Video": "Video",
    "Sticker": "Sticker",
    "Voice": "Voice",
}


class WhatsappService(Service):
    def __init__(self, username, api_key):
        super(WhatsappService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = "https://chat." + self._PRODUCTION_DOMAIN

    def send(
        self,
        body,
        wa_number,
        phone_number,
        callback=None,
    ):
        try:
            data = {
                "username": self._username,
                "waNumber": wa_number,
                "phoneNumber": phone_number,
                "body": body,
            }
            messageSchema = Schema(
                {
                    "username": And(str),
                    "waNumber": And(
                        str,
                        lambda s: validate_phone(s),
                        error=f"Invalid whatsapp number: {wa_number}",
                    ),
                    "phoneNumber": And(
                        str,
                        lambda s: validate_phone(s),
                        error=f"Invalid phone number: {phone_number}",
                    ),
                    "body": {
                        Optional("mediaType"): And(
                            str,
                            lambda s: s in mediaTypes,
                            error=f"Invalid media type, valid types are {list(mediaTypes.keys())}",
                        ),
                        Optional("url"): And(str),
                        Optional("caption"): And(str),
                        Optional("message"): And(str),
                        Optional("body"): {"text": And(str)},
                        Optional("header"): {"text": And(str)},
                        Optional("footer"): {"text": And(str)},
                    },
                }
            )
            data = messageSchema.validate(data)
        except SchemaError as err:
            raise ValueError(err)

        url = self._make_url("/whatsapp/message/send")
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
