
import unirest

unirest.timeout(30)


class AfricasTalkingException(Exception):
    pass


class Service(object):

    def __init__(self, username, api_key):

        self._PRODUCTION_DOMAIN = 'africastalking.com'
        self._SANDBOX_DOMAIN = 'sandbox.africastalking.com'

        self._username = username
        self._api_key = api_key
        self._headers = {
            'User-Agent': 'AfricasTalking-Python/2.x',
            'Accept': 'application/json',
            'ApiKey': self._api_key
        }
        self._baseUrl = 'https://api.' + self._PRODUCTION_DOMAIN

        self._init_service()

    def _is_sandbox(self):
        return self._username == 'sandbox'

    def _make_url(self, path):
        return self._baseUrl + path

    def _init_service(self):
        raise NotImplementedError

    @staticmethod
    def __make_get_request(url, headers, params, callback=None):
        return unirest.get(
            url=url,
            headers=headers,
            params=params,
            callback=callback,
        )

    @staticmethod
    def __make_post_request(url, headers, params, callback=None):
        return unirest.post(
            url=url,
            headers=headers,
            params=params,
            callback=callback,
        )

    def _make_request(self, url, method, headers, params, callback=None):
        method = method.upper()
        if callback is None:

            if method == 'GET':
                res = self.__make_get_request(url, headers, params)
            elif method == 'POST':
                res = self.__make_post_request(url, headers, params)
            else:
                raise AfricasTalkingException('Unexpected HTTP method: ' + method)

            if 200 <= res.code < 300:
                return res.body
            else:
                raise AfricasTalkingException(res.body)
        else:
            def cb(response):
                if 200 <= response.code < 300:
                    callback(None, response.body)
                else:
                    callback(AfricasTalkingException(response.body), None)

            if method == 'GET':
                return self.__make_get_request(url, headers, params, cb)
            elif method == 'POST':
                return self.__make_post_request(url, headers, params, cb)
            else:
                raise AfricasTalkingException('Unexpected HTTP method: ' + method)


class APIService(Service):

    def __init__(self, username, api_key):
        super(APIService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = 'https://api.'
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN
