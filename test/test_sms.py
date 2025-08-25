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
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
token_service = africastalking.Token
service = africastalking.SMS


class TestSmsService(unittest.TestCase):
    @responses.activate
    def test_send(self):
        responses.add(
            responses.POST,
            "https://api.africastalking.com/version1/messaging",
            json={
                "SMSMessageData": {
                    "Message": "Sent to 2/2 Total Cost: KES 0.8000",
                    "Recipients": [
                        {
                            "statusCode": 101,
                            "number": "+254718769882",
                            "status": "Success",
                            "cost": "KES 0.8000",
                            "messageId": "ATPid_SampleTxnId123",
                        },
                        {
                            "statusCode": 101,
                            "number": "+254718769881",
                            "status": "Success",
                            "cost": "KES 0.8000",
                            "messageId": "ATPid_SampleTxnId1234",
                        },
                    ],
                }
            },
            status=200,
        )
        res = service.send(
            "test_send()",
            ["+254718769882", "+254718769881"],
            enqueue=True,
            sender_id="AT2FA",
        )
        recipients = res["SMSMessageData"]["Recipients"]
        assert len(recipients) == 2
        assert recipients[0]["status"] == "Success"

    @responses.activate
    def test_heavy_single_send(self):
        count = 1000
        phone_numbers = list(
            map(lambda x: str("+254718" + str(x + count)), range(1, count))
        )
        recipients = []
        for i in range(len(phone_numbers)):
            recipients += {
                "statusCode": 101,
                "number": phone_numbers[i],
                "status": "Success",
                "cost": "KES 0.8000",
                "messageId": "ATPid_SampleTxnId123",
            }
        responses.add(
            responses.POST,
            "https://api.africastalking.com/version1/messaging",
            json={
                "SMSMessageData": {
                    "Message": f"Sent to {count}/{count} Total Cost: KES 0.8000",
                    "Recipients": recipients,
                }
            },
            status=200,
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

    @responses.activate
    def test_send_premium(self):
        responses.add(
            responses.POST,
            "https://content.africastalking.com/version1/messaging",
            json={
                "SMSMessageData": {
                    "Message": "Sent to 2/2 Total Cost: KES 0.8000",
                    "Recipients": [
                        {
                            "statusCode": 101,
                            "number": "+254718769882",
                            "status": "Success",
                            "cost": "KES 0.8000",
                            "messageId": "ATPid_SampleTxnId123",
                        },
                        {
                            "statusCode": 101,
                            "number": "+254718769881",
                            "status": "Success",
                            "cost": "KES 0.8000",
                            "messageId": "ATPid_SampleTxnId1234",
                        },
                    ],
                }
            },
            status=200,
        )
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

    @responses.activate
    def test_fetch_messages(self):
        responses.add(
            responses.GET,
            f"https://api.africastalking.com/version1/messaging?username={USERNAME}&lastReceivedId=0",
            json={
                "SMSMessageData": {
                    "Messages": [
                        {
                            "linkId": "SampleLinkId123",
                            "text": "Hello",
                            "to": "28901",
                            "id": 15071,
                            "date": "2018-03-19T08:34:18.445Z",
                            "from": "+254711XXXYYY",
                        }
                    ]
                }
            },
            status=200,
        )
        res = service.fetch_messages(0)
        assert len(res) >= 0

    @responses.activate
    def test_create_safaricom_subscription(self):
        responses.add(
            responses.POST,
            "https://content.africastalking.com/version1/subscription/safaricom",
            json={
                "responseCode": "Success",
                "status": "Sent",
                "transactionId": "Tid_3886639048695350000",
                "url": "https://dcbatf2.safaricom.co.ke/v2/service/safaricom/bluu/Tid_177539048695398400?onError=https%3A%2F%2Fmidge-driven-flamingo.ngrok-free.app%2Fcontent%2Fpremium%2Fevina%2Fsubscription%3Ftype%3DERR%26rId%3DrequestId-9168bb62-3b6a-4a87-811d-4ef4c7e1e6dd",
            },
            status=200,
        )
        res = service.create_safaricom_subscription(
            short_code="78942",
            keyword="KiKi",
            phone_number="+254718769882",
            redirect_url="http://test.test",
        )
        assert res["responseCode"] == "Success"


if __name__ == "__main__":
    unittest.main()
