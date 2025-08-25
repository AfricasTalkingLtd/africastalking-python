"""
Whatsapp

send(): Send Whatsapp message.
"""

import africastalking
import unittest
import responses
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Whatsapp


class TestWhatsappService(unittest.TestCase):
    @responses.activate
    def test_send_whatsapp(self):
        responses.add(
            responses.POST,
            "https://chat.africastalking.com/whatsapp/message/send",
            json={
                "messageId": "ATXid_91292754713251840",
                "phoneNumber": "+254700000000",
                "status": "SENT",
            },
            status=200,
        )
        res = service.send({"message": "test"}, "+254700000000", "+25471111111")
        assert res["status"] == "SENT"


if __name__ == "__main__":
    unittest.main()
