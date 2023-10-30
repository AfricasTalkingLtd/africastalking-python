"""
SMS

send(message: String, recipients: List<String>, senderId: Optional<String>, enqueue: Optional<Boolean>): Send a bulk message to recipients, optionally from senderId (Short Code or Alphanumeric).

sendPremium(message: String, keyword: String, linkId: String, recipients: List<String>, senderId: Optional<String>, retryDurationInHours: Optional<Integer>): Send a premium SMS

fetchMessages(lastReceivedId: Optional<Integer>): Fetch your messages

fetchSubscriptions(shortCode: String, keyword: String, lastReceivedId: Optional<Integer>): Fetch your premium subscription data

createSubscription(shortCode: String, keyword: String, phoneNumber: String): Create a premium subscription
"""
import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
token_service = africastalking.Token
service = africastalking.SMS


class TestSmsService(unittest.TestCase):
    def test_send(self):
        res = service.send(
            "test_send()",
            ["+254718769882", "+254718769881"],
            enqueue=True,
            sender_id="AT2FA",
        )
        recipients = res["SMSMessageData"]["Recipients"]
        assert len(recipients) == 2
        assert recipients[0]["status"] == "Success"

    def test_heavy_single_send(self):
        count = 100000
        phone_numbers = list(
            map(lambda x: str("+254718" + str(x + count)), range(1, count))
        )

        def on_finish(error, data):
            if error:
                raise error
            recipients = data["SMSMessageData"]["Recipients"]
            assert len(recipients) <= count

        service.send(
            "test_heavy_single_send()",
            phone_numbers,
            enqueue=True,
            sender_id="AT2FA",
            callback=on_finish,
        )

    def test_send_premium(self):
        res = service.send_premium(
            "test_send_premium()",
            "AT2FA",
            ["+254718769882", "+254718769881"],
            "KiKi",
            "Linky",
            retry_duration_in_hours=10,
        )
        recipients = res["SMSMessageData"]["Recipients"]
        assert len(recipients) == 2
        assert recipients[0]["status"] == "Success"

    def test_fetch_messages(self):
        res = service.fetch_messages(0)
        assert len(res) >= 0

    def test_fetch_subscriptions(self):
        res = service.fetch_subscriptions(
            short_code=13715, keyword="KiKi", last_received_id=0
        )
        assert len(res) >= 0

    def test_create_subscription(self):
        res = service.create_subscription(
            short_code=13715, keyword="KiKi", phone_number="+254718769882"
        )
        assert res["description"] == "Waiting for user input"

    def test_delete_subscription(self):
        res = service.delete_subscription(
            short_code=13715, keyword="KiKi", phone_number="+254718769882"
        )
        assert res["status"] == "Success"


if __name__ == "__main__":
    unittest.main()
