from Service import APIService


class AccountService(APIService):
    def __init__(self, username, api_key):
        super(AccountService, self).__init__(username, api_key)

    def _init_service(self):
        super(AccountService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1'

    def fetch_account(self, callback=None):
        url = self._make_url('/user')
        params = {
            'username': self._username
        }
        return self._make_request(url, 'GET', headers=self._headers, params=params, callback=callback)
