from schema import Schema, And, SchemaError
import json
from Service import APIService, AfricasTalkingException, validate_amount


class AirtimeService(APIService):
    def __init__(self, username, api_key):
        super(AirtimeService, self).__init__(username, api_key)

    def _init_service(self):
        super(AirtimeService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1/airtime'

    def send(self, phone_number=None, amount=None, recipients=None, callback=None):

        if phone_number is not None and amount is not None:
            recipients = [
                {'phoneNumber': phone_number, 'amount': amount},
            ]

        try:
            schema = Schema([
                {
                    'phoneNumber': And(str, len),
                    'amount': And(str, lambda s: validate_amount(s))
                }
            ])
            recipients = schema.validate(recipients)
        except SchemaError as err:
            raise AfricasTalkingException('Invalid recipients: ' + err.message)

        url = self._make_url('/send')
        params = {
            'username': self._username,
            'recipients': json.dumps(recipients)
        }
        return self._make_request(url, 'POST', headers=self._headers, params=params, callback=callback)
