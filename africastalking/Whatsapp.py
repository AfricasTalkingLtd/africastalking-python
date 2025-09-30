import json
import warnings
from .Service import Service, validate_phone
from schema import Schema, And, Optional, SchemaError


media_types = {
    "Image": "Image",
    "Audio": "Audio",
    "Video": "Video",
    "Sticker": "Sticker",
    "Voice": "Voice",
}

header_types = {
    "MEDIA": "MEDIA",
    "TEXT": "TEXT",
    "LOCATION": "LOCATION",
}

button_types = {
    "PHONE_NUMBER": "PHONE_NUMBER",
    "URL": "URL",
    "QUICK_REPLY": "QUICK_REPLY",
}


class WhatsappService(Service):
    def __init__(self, username, api_key):
        super(WhatsappService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = "https://chat." + self._PRODUCTION_DOMAIN
        if self._is_sandbox():
            warnings.warn(
                "Sandbox is currently not available for the Whatsapp service."
            )

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
                            lambda s: s in media_types,
                            error=f"Invalid media type, valid types are {list(media_types.keys())}",
                        ),
                        Optional("url"): And(
                            str,
                            lambda s: "mediaType" in body,
                            error="mediaType required for url key",
                        ),
                        Optional("caption"): And(
                            str,
                            lambda s: "url" in body,
                            error="url required for caption key",
                        ),
                        Optional("message"): And(
                            str,
                            lambda s: "mediaType" not in body,
                            error="mediaType cannot be used with message key",
                        ),
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

    def send_template(
        self,
        components,
        wa_number,
        name,
        language,
        category,
        callback=None,
    ):
        try:
            data = {
                "username": self._username,
                "waNumber": wa_number,
                "name": name,
                "language": language,
                "category": category,
                "components": components,
            }
            messageSchema = Schema(
                {
                    "username": And(str),
                    "waNumber": And(
                        str,
                        lambda s: validate_phone(s),
                        error=f"Invalid whatsapp number: {wa_number}",
                    ),
                    "name": And(str),
                    "language": And(str),
                    "category": And(str),
                    "components": {
                        Optional("header"): {
                            "type": And(
                                str,
                                lambda s: s in header_types,
                                error=f"Invalid header type, valid types are {list(header_types.keys())}",
                            ),
                            "format": And(str),
                            "text": And(str),
                            "example": {"header_text": And(list)},
                        },
                        "body": {
                            "type": And(str),
                            "text": And(str),
                            "example": {"body_text": And(list)},
                        },
                        Optional("footer"): {
                            "type": And(str),
                            "text": And(str),
                        },
                        Optional("buttons"): {
                            "type": And(
                                str,
                                lambda s: s in button_types,
                                error=f"Invalid button type, valid types are {list(button_types.keys())}",
                            ),
                            "url": And(str),
                            "text": And(str),
                            "phoneNumber": And(str),
                            "example": And(list),
                        },
                    },
                }
            )
            data = messageSchema.validate(data)
        except SchemaError as err:
            raise ValueError(err)

        url = self._make_url("whatsapp/template/send")
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
