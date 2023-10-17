from .Service import ChatService, validate_phone
from schema import Schema, And, Optional, SchemaError


chatTypes = {"whatsapp": "WhatsApp", "telegram": "Telegram"}

messageTypes = {"text": "Text", "media": "Media", "location": "Location"}

mediaTypes = {
    "image": "Image",
    "audio": "Audio",
    "video": "Video",
    "sticker": "Sticker",
    "voice": "Voice",
}


class WhatsappService(ChatService):
    def __init__(self, username, api_key):
        super(WhatsappService, self).__init__(username, api_key)

    def _init_service(self):
        super(WhatsappService, self)._init_service()

    def send(self, message, product_id, channel_number, customer_number, channel):
        data = {
            "username": self._username,
            "productId": product_id,
            "channelNumber": channel_number,
            "channel": channel,
            "customerNumber": customer_number,
            "body": message,
        }
        messageSchema = Schema(
            [
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
            ]
        )
        data = messageSchema.validate(data)

        url = self._make_url("/message/send")

        return self._make_request(
            url, "POST", headers=self._headers, params=None, data=data
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
