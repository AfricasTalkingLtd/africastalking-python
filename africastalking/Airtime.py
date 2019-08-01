import json
from . Service import APIService, validate_amount, validate_phone, validate_currency


class AirtimeService(APIService):
    def __init__(self, username, api_key):
        super(AirtimeService, self).__init__(username, api_key)

    def _init_service(self):
        super(AirtimeService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1/airtime'

    def send(self, phone_number=None, amount=None, currency_code=None, recipients=None, callback=None):

        def join_amount_and_currency(obj):
                obj['amount'] = " ".join([str(obj['currency_code']), str(obj['amount'])])
                del obj['currency_code']
                return obj

        def value_validator(phoneNumber, amount, currency_code):
            if not validate_phone(phoneNumber):
                return 'Invalid phone number'
            elif not validate_amount(amount):
                return 'Invalid amount' 
            elif not validate_currency(currency_code):
                return 'Invalid currency code'
            else:
                return False              

        
        if recipients is None:
            recipients= [
                {'phoneNumber': str(phone_number), 'amount': str(amount), 'currency_code': str(currency_code)}
            ]            
        
        for recipient in recipients:
            if not set(recipient.keys()) == {'phoneNumber', 'amount', 'currency_code'}:
                raise(ValueError("must specify phoneNumber, currencyCode and amount for recipient: %s" %(recipient))) 

            else:
                phoneNumber = recipient['phoneNumber']
                amount = recipient['amount']
                currency_code = recipient['currency_code']
                validation_err = value_validator(phoneNumber, amount, currency_code)

                if validation_err:
                    raise(ValueError("Recipient data error: %s in %s" %(validation_err, recipient)))
                else:
                    join_amount_and_currency(recipient) 

        url = self._make_url('/send')
        data = {
            'username': self._username,
            'recipients': json.dumps(recipients)
        }
        return self._make_request(url, 'POST', headers=self._headers, params=None, data=data, callback=callback)
