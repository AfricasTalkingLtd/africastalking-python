import re
import json
from schema import Schema, And, SchemaError, Optional
from Service import Service, AfricasTalkingException, validate_amount


class PaymentService(Service):
    Bank = {
        'FCMB_NG': 234001,
        'Zenith_NG': 234002,
        'Access_NG': 234003,
        'GTBank_NG': 234004,
        'Ecobank_NG': 234005,
        'Diamond_NG': 234006,
        'Providus_NG': 234007,
        'Unity_NG': 234008,
        'Stanbic_NG': 234009,
        'Sterling_NG': 234010,
        'Parkway_NG': 234011,
        'Afribank_NG': 234012,
        'Enterprise_NG': 234013,
        'Fidelity_NG': 234014,
        'Heritage_NG': 234015,
        'Keystone_NG': 234016,
        'Skye_NG': 234017,
        'Stanchart_NG': 234018,
        'Union_NG': 234019,
        'Uba_NG': 234020,
        'Wema_NG': 234021,
        'First_NG': 234022,
        'CBA_KE': 254001,
        'UNKNOWN': -1,
    }
    
    def __init__(self, username, api_key):
        super(PaymentService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = 'https://payments.'
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN

    def mobile_checkout(self, product_name, phone_number, amount, metadata={}, callback=None):

        if not validate_amount(amount):
            raise AfricasTalkingException('Invalid amount')

        amount = amount.split(' ')
        url = self._make_url('/mobile/checkout/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = json.dumps({
            'username': self._username,
            'productName': product_name,
            'phoneNumber': phone_number,
            'currencyCode': amount[0],
            'amount': amount[1],
            'metadata': metadata
        })
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)

    def mobile_b2c(self, product_name, consumers, callback=None):

        try:
            reasons = ('SalaryPayment',
                       'SalaryPaymentWithWithdrawalChargePaid',
                       'BusinessPayment',
                       'BusinessPaymentWithWithdrawalChargePaid',
                       'PromotionPayment')
            schema = Schema([
                {
                    'name': And(str, len),
                    'phoneNumber': And(str, len),
                    'currencyCode': And(str, lambda s: len(s) == 3),
                    'amount': And(lambda f: float(f) > 0),
                    Optional('providerChannel'): And(str, len),
                    Optional('reason'): And(str, lambda s: s in reasons),
                    Optional('metadata'): And(dict)
                }
            ])
            consumers = schema.validate(consumers)
        except SchemaError as err:
            raise AfricasTalkingException('Invalid consumers: ' + err.message)

        url = self._make_url('/mobile/b2c/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = json.dumps({
            'username': self._username,
            'productName': product_name,
            'recipients': consumers
        })
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)

    def mobile_b2b(self, product_name, business, callback=None):

        try:
            providers = ('Mpesa', 'Athena')
            types = ('BusinessBuyGoods',
                     'BusinessPayBill',
                     'DisburseFundsToBusiness',
                     'BusinessToBusinessTransfer')
            schema = Schema({
                'provider': And(str, lambda s: s in providers),
                'transferType': And(str, lambda s: s in types),
                'currencyCode': And(str, lambda s: len(s) == 3),
                'amount': And(lambda f: float(f) > 0),
                'destinationChannel': And(str, len),
                'destinationAccount': And(str, len),
                Optional('metadata'): And(dict)
            })
            business = schema.validate(business)
        except SchemaError as err:
            raise AfricasTalkingException('Invalid business: ' + err.message)

        url = self._make_url('/mobile/b2b/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = business.copy()
        params.update({
            'username': self._username,
            'productName': product_name,
        })
        params = json.dumps(params)
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)

    def bank_transfer(self, product_name, recipients, callback=None):

        try:
            bank_account_schema = Schema({
                'accountNumber': And(str, len),
                'bankCode': And(int, lambda i: i in PaymentService.Bank.values()),
                Optional('accountName'): And(str, len),
            })
            schema = Schema([{
                'bankAccount': And(dict, lambda s: bank_account_schema.validate(s)),
                'currencyCode': And(str, lambda s: len(s) == 3),
                'amount': And(lambda f: float(f) > 0),
                'narration': And(str, len),
                Optional('metadata'): And(dict)
            }])
            recipients = schema.validate(recipients)
        except SchemaError as err:
            raise AfricasTalkingException('Invalid recipients: ' + err.message)

        url = self._make_url('/bank/transfer')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = {
            'username': self._username,
            'productName': product_name,
            'recipients': recipients,
        }
        params = json.dumps(params)
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)

    def bank_checkout(self, product_name, amount, bank_account, narration, metadata={}, callback=None):

        if not validate_amount(amount):
            raise AfricasTalkingException('Invalid amount')

        if narration is None:
            raise AfricasTalkingException('Invalid narration')

        try:
            bank_account_schema = Schema({
                'accountNumber': And(str, len),
                'bankCode': And(int, lambda i: i in PaymentService.Bank.values()),
                Optional('accountName'): And(str, len),
                Optional('dateOfBirth'): And(str, lambda date: re.match('(\d{4})-(\d{2})-(\d{2})$', date))
            })
            bank_account = bank_account_schema.validate(bank_account)
        except SchemaError as err:
            raise AfricasTalkingException('Invalid recipients: ' + err.message)

        amount = amount.split(' ')
        url = self._make_url('/bank/checkout/charge')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = {
            'username': self._username,
            'productName': product_name,
            'bankAccount': bank_account,
            'currencyCode': amount[0],
            'amount': amount[1],
            'narration': str(narration),
            'metadata': metadata,
        }
        params = json.dumps(params)
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)

    def __validate_checkout(self, checkout_type, transaction_id, otp, callback=None):

        assert checkout_type in ('bank', 'card')

        url = self._make_url('/' + checkout_type + '/checkout/validate')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = {
            'username': self._username,
            'transactionId': str(transaction_id),
            'otp': str(otp),
        }
        params = json.dumps(params)
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)

    def validate_bank_checkout(self, transaction_id, otp, callback=None):
        return self.__validate_checkout('bank', transaction_id, otp, callback)

    def validate_card_checkout(self, transaction_id, otp, callback=None):
        return self.__validate_checkout('card', transaction_id, otp, callback)

    def card_checkout(self, product_name, amount, narration,
                      payment_card=None, checkout_token=None, metadata={}, callback=None):

        if not validate_amount(amount):
            raise AfricasTalkingException('Invalid amount')

        if narration is None:
            raise AfricasTalkingException('Invalid narration')

        if payment_card is None and checkout_token is None:
            raise AfricasTalkingException('You need to provide either checkout_token or payment_card')

        countries = ('NG')
        amount = amount.split(' ')
        url = self._make_url('/card/checkout/charge')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = {
            'username': self._username,
            'productName': product_name,
            'currencyCode': amount[0],
            'amount': amount[1],
            'narration': str(narration),
            'metadata': metadata,
        }

        if payment_card is not None:
            try:
                payment_card_schema = Schema({
                    'number': And(str, len),
                    'countryCode': And(str, lambda i: i in countries),
                    'cvvNumber': And(int),
                    'expiryMonth': And(int, lambda i: 1 <= i <= 12),
                    'expiryYear': And(int, lambda i: i >= 2018),
                    'authToken': And(str, len),
                })
                payment_card = payment_card_schema.validate(payment_card)
                params['paymentCard'] = payment_card
            except SchemaError as err:
                raise AfricasTalkingException('Invalid recipients: ' + err.message)
        else:
            params['checkoutToken'] = checkout_token

        params = json.dumps(params)
        return self._make_request(url, 'POST', headers=headers, params=params, callback=callback)
