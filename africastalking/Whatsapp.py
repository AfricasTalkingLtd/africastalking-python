from .Service import ChatService, validate_phone, validate_keys


class WhatsappService(ChatService):
    def __init__(self, username, api_key):
        super(WhatsappService, self).__init__(username, api_key)

    def _init_service(self):
        super(WhatsappService, self)._init_service()

    def send(
        self, message, product_id, channel_number, customer_number, channel="Whatsapp"
    ):

        if not validate_phone(customer_number):
            raise ValueError("Invalid phone number: " + customer_number)

        if not validate_phone(channel_number):
            raise ValueError("Invalid channel number: " + channel_number)

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

    def opt_in(self, channel_number, customer_number, channel="Whatsapp"):
        url = self._make_url("/chat/consent")
        data = {
            "username": self._username,
            "channelNumber": channel_number,
            "channel": channel,
            "customerNumber": customer_number,
            "action": "OptIn",
        }

        return self._make_request(
            url, "POST", headers=self._headers, params=None, data=data
        )

    def opt_out(self, channel_number, customer_number, channel="Whatsapp"):
        url = self._make_url("/chat/consent")
        data = {
            "username": self._username,
            "channelNumber": channel_number,
            "channel": channel,
            "customerNumber": customer_number,
            "action": "OptOut",
        }

        return self._make_request(
            url, "POST", headers=self._headers, params=None, data=data
        )

    def send_template(
        self, message, product_id, channel_number, customer_number, channel="Whatsapp"
    ):

        if not validate_phone(customer_number):
            raise ValueError("Invalid phone number: " + customer_number)

        if not validate_phone(channel_number):
            raise ValueError("Invalid channel number: " + channel_number)

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
