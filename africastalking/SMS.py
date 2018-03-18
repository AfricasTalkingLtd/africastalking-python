from .Service import APIService, validate_phone


class SMSService(APIService):
    def __init__(self, username, api_key):
        super(SMSService, self).__init__(username, api_key)

    def _init_service(self):
        super(SMSService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1'

    def send(self, message, recipients, sender_id=None, enqueue=False, callback=None):

        for phone in recipients:
            if not validate_phone(phone):
                raise ValueError('Invalid phone number: ' + phone)

        url = self._make_url('/messaging')
        data = {
            'username': self._username,
            'to': ','.join(recipients),
            'message': message,
            'bulkSMSMode': 1,
        }

        if sender_id is not None:
            data['from'] = sender_id

        if enqueue:
            data['enqueue'] = 1

        return self._make_request(url, 'POST', headers=self._headers, params=None, data=data, callback=callback)

    def send_premium(self, message, keyword, link_id, recipients, sender_id=None,
                     retry_duration_in_hours=None, callback=None):

        for phone in recipients:
            if not validate_phone(phone):
                raise ValueError('Invalid phone number: ' + phone)

        url = self._make_url('/messaging')
        data = {
            'username': self._username,
            'to': ','.join(recipients),
            'message': message,
            'bulkSMSMode': 0,
            'keyword': keyword,
            'linkId': link_id
        }

        if sender_id is not None:
            data['from'] = sender_id

        if retry_duration_in_hours is not None:
            data['retryDurationInHours'] = retry_duration_in_hours

        return self._make_request(url, 'POST', headers=self._headers, params=None, data=data, callback=callback)

    def fetch_messages(self, last_received_id=None, callback=None):
        url = self._make_url('/messaging')
        params = {
            'username': self._username
        }

        if last_received_id is not None:
            params['lastReceivedId'] = last_received_id

        return self._make_request(url, 'GET', headers=self._headers, params=params, data=None, callback=callback)

    def fetch_subscriptions(self, short_code, keyword, last_received_id=None, callback=None):
        url = self._make_url('/subscription')
        params = {
            'username': self._username,
            'shortCode': short_code,
            'keyword': keyword
        }

        if last_received_id is not None:
            params['lastReceivedId'] = last_received_id

        return self._make_request(url, 'GET', headers=self._headers, params=params, data=None, callback=callback)

    def create_subscription(self, short_code, keyword, phone_number, checkout_token, callback=None):

        if not validate_phone(phone_number):
            raise ValueError('Invalid phone number')

        url = self._make_url('/subscription/create')
        data = {
            'username': self._username,
            'shortCode': short_code,
            'keyword': keyword,
            'phoneNumber': phone_number,
            'checkoutToken': checkout_token,
        }

        return self._make_request(url, 'POST', headers=self._headers, data=data, params=None, callback=callback)

