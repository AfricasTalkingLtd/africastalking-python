from schema import Schema, And, SchemaError
import json
from . Service import APIService, validate_amount, validate_phone


class AirtimeService(APIService):
    def __init__(self, username, api_key):
        super(AirtimeService, self).__init__(username, api_key)

    def _init_service(self):
        super(AirtimeService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1/airtime'

    def send(self, phone_number=None, amount=None, recipients=None, callback=None):

        if phone_number is not None and amount is not None:
            recipients = [
                {'phoneNumber': str(phone_number), 'amount': str(amount)},
            ]

        try:
            schema = Schema([
                {
                    'phoneNumber': And(str, lambda s: validate_phone(s)),
                    'amount': And(str, lambda s: validate_amount(s))
                }
            ])
            recipients = schema.validate(recipients)
        except SchemaError as err:
            raise ValueError('Invalid recipients: ' + err.message)

        url = self._make_url('/send')
        data = {
            'username': self._username,
            'recipients': json.dumps(recipients)
        }
        return self._make_request(url, 'POST', headers=self._headers, params=None, data=data, callback=callback)
