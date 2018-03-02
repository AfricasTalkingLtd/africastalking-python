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
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Voice


class TestVoiceService(unittest.TestCase):

    def test_call(self):
        res = service.call(source="+254718769881", destination="+254718769880")
        assert res['errorMessage'] != 'None'

    def test_fetch_queued_calls(self):
        res = service.fetch_queued_calls(phone_number='+254718769880')
        assert res['status'] == 'Success'

    def test_media_upload(self):
        res = service.media_upload(phone_number='+254718769889', url='https://aksalj.com')
        assert res == 'The request has been fulfilled and resulted in a new resource being created.'


if __name__ == '__main__':
    unittest.main()
