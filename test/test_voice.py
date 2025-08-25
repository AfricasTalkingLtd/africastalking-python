"""
Voice

call(phoneNumber: String): Initiate a phone call

fetchQueuedCalls(phoneNumber: String): Get queued calls

uploadMediaFile(phoneNumber: String, url: String): Upload voice media file

ActionBuilder: Build voice xml when callback URL receives a POST from the voice API
    say(text: String)

    play(url: String)

    getDigits(text: String, url: String, numDigits: Integer, timeout: Integer, finishOnKey: String, callbackUrl: String)

    dial(phoneNumbers: String, ringbackTone: String, record: Boolean, sequential: Boolean, callerId: String, maxDuration: Integer)

    conference()

    record()

    record(String text, URL url, int maxLength, long timeout, String finishOnKey, boolean trimSilence, boolean playBeep, URL callbackUrl)

    enqueue()

    dequeue()

    reject()

    redirect()

    build(): Finally build the xml

"""

import africastalking
import responses
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Voice


class TestVoiceService(unittest.TestCase):
    @responses.activate
    def test_call(self):
        responses.add(
            responses.POST,
            "https://voice.africastalking.com/call",
            json={
                "entries": [
                    {
                        "phoneNumber": "+234XXXYYYZZZZ",
                        "status": "Queued",
                        "sessionId": "ATVId_abcdef",
                    }
                ],
                "errorMessage": "None",
            },
            status=200,
        )
        res = service.call(
            callFrom="+254711223355", callTo=["+254711223366", "+254711223344"]
        )
        assert res["errorMessage"] == "None"

    @responses.activate
    def test_fetch_queued_calls(self):
        responses.add(
            responses.POST,
            "https://voice.africastalking.com/queueStatus",
            json={
                "status": "Success",
                "entries": [
                    {"phoneNumber": "+254711223366", "queueName": "", "numCalls": 1}
                ],
                "errorMessage": "None",
            },
            status=200,
        )
        res = service.fetch_queued_calls(phone_number="+254711223366")

        assert res["status"] == "Success"

    @responses.activate
    def test_media_upload(self):
        responses.add(
            responses.POST,
            "https://voice.africastalking.com/mediaUpload",
            json={
                "success": True,
            },
            status=201,
        )
        res = service.media_upload(
            phone_number="+254711223355", url="https://aksalj.com"
        )
        assert res["success"]


if __name__ == "__main__":
    unittest.main()
