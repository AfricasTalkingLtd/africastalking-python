from Service import Service


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
        url = self._make_url('/call')
        params = {
            'username': self._username,
            'from': source,
            'to': destination,
        }
        return self._make_request(url, 'POST', headers=self._headers, params=params, callback=callback)

    def fetch_queued_calls(self, phone_numbers, callback=None):
        url = self._make_url('/queueStatus')
        params = {
            'username': self._username,
            'phoneNumbers': phone_numbers,
        }
        return self._make_request(url, 'POST', headers=self._headers, params=params, callback=callback)

    def media_upload(self, phone_number, url, callback=None):
        call_url = self._make_url('/mediaUpload')
        params = {
            'username': self._username,
            'phoneNumber': phone_number,
            'url': url,
        }
        return self._make_request(call_url, 'POST', headers=self._headers, params=params, callback=callback)
