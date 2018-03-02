from Service import Service, validate_phone


class VoiceService(Service):
    def __init__(self, username, api_key):
        super(VoiceService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = 'https://voice.'
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN

    def call(self, source, destination, callback=None):

        if not validate_phone(destination):
            raise ValueError('Invalid destination phone number')

        url = self._make_url('/call')
        data = {
            'username': self._username,
            'from': source,
            'to': destination,
        }
        return self._make_request(url, 'POST', headers=self._headers, params=None, data=data, callback=callback)

    def fetch_queued_calls(self, phone_number, callback=None):

        if not validate_phone(phone_number):
            raise ValueError('Invalid phone number')

        url = self._make_url('/queueStatus')
        data = {
            'username': self._username,
            'phoneNumbers': phone_number,
        }
        return self._make_request(url, 'POST', headers=self._headers, params=None, data=data, callback=callback)

    def media_upload(self, phone_number, url, callback=None):

        if not validate_phone(phone_number):
            raise ValueError('Invalid phone number')

        call_url = self._make_url('/mediaUpload')
        data = {
            'username': self._username,
            'phoneNumber': phone_number,
            'url': url,
        }
        return self._make_request(call_url, 'POST', headers=self._headers, params=None, data=data, callback=callback)
