from Service import APIService


class ApplicationService(APIService):
    def __init__(self, username, api_key):
        super(ApplicationService, self).__init__(username, api_key)

    def _init_service(self):
        super(ApplicationService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1'

    def fetch_application_data(self, callback=None):
        url = self._make_url('/user')
        params = {
            'username': self._username
        }
        return self._make_request(url, 'GET', headers=self._headers, params=params, data=None, callback=callback)
