from .Service import ChatService, validate_phone, validate_keys
from enum import Enum, EnumMeta


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__.values()


class ChatServices(Enum, metaclass=EnumMeta):
    WHATSAPP = "WhatsApp"
    TELEGRAM = "Telegram"


class MessageType(Enum, metaclass=EnumMeta):
    TEXT = "Text"
    MEDIA = "Media"
    LOCATION = "Location"


class MediaType(Enum, metaclass=EnumMeta):
    IMAGE = "Image"
    AUDIO = "Audio"
    VIDEO = "Video"
    DOCUMENT = "Document"
    STICKER = "Sticker"
    VOICE = "Voice"


class WhatsappService(ChatService):
    def __init__(self, username, api_key):
        super(WhatsappService, self).__init__(username, api_key)

    def _init_service(self):
        super(WhatsappService, self)._init_service()

    def send(self, message, product_id, channel_number, customer_number, channel):
        if not channel in ChatServices:
            raise ValueError(
                f"Invalid channel, accepted channels are: {ChatServices._member_names_}"
            )

        if channel == ChatServices.WHATSAPP:
            if not validate_phone(customer_number):
                raise ValueError("Invalid phone number: " + customer_number)

            if not validate_phone(channel_number):
                raise ValueError("Invalid channel number: " + channel_number)

        if not validate_keys(message, {"type"}) or not message["type"] in MessageType:
            raise (
                ValueError(
                    f"Must specify valid message type: {MessageType._member_names_}"
                )
            )

        if message["type"] == MessageType.MEDIA:
            if (
                not message["media"]
                or not message["media"] in MediaType
            ):
                raise (
                    ValueError(
                        f"Must specify valid media type: {MediaType._member_names_}"
                    )
                )

        url = self._make_url("/message/send")
        data = {
            "username": self._username,
            "productId": product_id,
            "channelNumber": channel_number,
            "channel": channel,
            "customerNumber": customer_number,
            "body": message,
        }

        return self._make_request(
            url, "POST", headers=self._headers, params=None, data=data
        )

    def consent_response(self, channel_number, customer_number, channel, opt_in):
        if not channel in ChatServices:
            raise ValueError(
                f"Invalid channel, accepted channels are: {ChatServices._member_names_}"
            )
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
