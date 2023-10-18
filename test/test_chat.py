"""
Chat

send(message: String, productId: String, channel_number: String, customer_number: String, channel: string): Send a message to a single recipient, using a specific channel and channel number.

consent_response(channel_number: String, customer_number: String, channel: string): Opts in or out of receiving messages.

send_template(message: String, productId: String, channel_number: String, customer_number: String, channel: string): Send a message to a single recipient, using a specific channel and channel number and template.

"""
import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
token_service = africastalking.Token
service = africastalking.Chat


class TestChatService(unittest.TestCase):
    def test_send(self):
        res = service.send(
            message={"type": "text", "text": "this is a test"},
            product_id="test",
            channel_number="+254123456789",
            customer_number="+254987654321",
            channel="whatsapp",
        )
        assert res["status"] == "Sent"

    def test_consent_response(self):
        res = service.consent_response(
            channel_number="+254123456789",
            customer_number="+254987654321",
            channel="whatsapp",
            opt_in=True,
        )
        assert res["status"] == "OptInRequestSent"

    def test_send_template(self):
        res = service.send_templaye(
            message={"type": "text", "text": "this is a test"},
            product_id="test",
            channel_number="+254123456789",
            customer_number="+254987654321",
            channel="whatsapp",
        )
        assert res["status"] == "Sent"


if __name__ == "__main__":
    unittest.main()
