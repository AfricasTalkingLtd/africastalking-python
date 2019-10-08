import re
import json
from schema import Schema, And, Optional
from . Service import Service, validate_phone, validate_data_units, validate_data_validity


class PaymentService(Service):
    BANK = {
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

    PROVIDER = {
        'Athena': 'Athena',
        'Mpesa': 'Mpesa'
    }

    TRANSFER_TYPE = {
        'BusinessBuyGoods': 'BusinessBuyGoods',
        'BusinessPayBill': 'BusinessPayBill',
        'DisburseFundsToBusiness': 'DisburseFundsToBusiness',
        'BusinessToBusinessTransfer': 'BusinessToBusinessTransfer'
    }

    REASON = {
        'SalaryPayment': 'SalaryPayment',
        'SalaryPaymentWithWithdrawalChargePaid': 'SalaryPaymentWithWithdrawalChargePaid',
        'BusinessPayment': 'BusinessPayment',
        'BusinessPaymentWithWithdrawalChargePaid': 'BusinessPaymentWithWithdrawalChargePaid',
        'PromotionPayment': 'PromotionPayment'
    }
    
    def __init__(self, username, api_key):
        super(PaymentService, self).__init__(username, api_key)

    def _init_service(self):
        self._baseUrl = 'https://payments.'
        if self._is_sandbox():
            self._baseUrl += self._SANDBOX_DOMAIN
        else:
            self._baseUrl += self._PRODUCTION_DOMAIN

    def mobile_checkout(self, product_name, phone_number, currency_code, amount, metadata={},
                        provider_channel=None, callback=None):

        if not validate_phone(phone_number):
            raise ValueError('Invalid phone number.')

        url = self._make_url('/mobile/checkout/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'phoneNumber': phone_number,
            'currencyCode': currency_code,
            'amount': amount,
            'metadata': metadata
        }
        if provider_channel is not None:
                data['providerChannel'] = provider_channel
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def mobile_b2c(self, product_name, consumers, callback=None):

        reasons = PaymentService.REASON.values()
        schema = Schema([
            {
                'name': And(str, len),
                'phoneNumber': And(str, lambda s: validate_phone(s)),
                'currencyCode': And(str, lambda s: len(s) == 3),
                'amount': And(lambda f: float(f) > 0),
                Optional('providerChannel'): And(str, len),
                Optional('reason'): And(str, lambda s: s in reasons),
                Optional('metadata'): And(dict)
            }
        ])
        consumers = schema.validate(consumers)
        url = self._make_url('/mobile/b2c/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = json.dumps({
            'username': self._username,
            'productName': product_name,
            'recipients': consumers
        })
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def mobile_b2b(self, product_name, business, callback=None):

        providers = PaymentService.PROVIDER.values()
        types = PaymentService.TRANSFER_TYPE.values()
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
        url = self._make_url('/mobile/b2b/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = business.copy()
        data.update({
            'username': self._username,
            'productName': product_name,
        })
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def mobile_data(self, product_name, recipients, callback=None):

        schema = Schema([{
            'phoneNumber': And(str, lambda s: validate_phone(s)),
            'quantity': And(lambda f: float(f) > 0),
            'unit': And(str, lambda s: validate_data_units(s)),
            'validity': And(str, lambda s: validate_data_validity(s)),
            Optional('metadata'): And(dict)
        }])
        recipients = schema.validate(recipients)
        url = self._make_url('/mobile/data/request')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'recipients': recipients,
        }
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)
        
    def bank_transfer(self, product_name, recipients, callback=None):

        bank_account_schema = Schema({
            'accountNumber': And(str, len),
            'bankCode': And(int, lambda i: i in PaymentService.BANK.values()),
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
        url = self._make_url('/bank/transfer')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'recipients': recipients,
        }
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def wallet_transfer(self, product_name, target_product_code, currency_code, amount, metadata = {}, callback=None):
        
        url = self._make_url('/transfer/wallet')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'targetProductCode': target_product_code,
            'currencyCode': currency_code,
            'amount': amount,
            'metadata': metadata
        }
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def topup_stash(self, product_name, currency_code, amount, metadata = {}, callback=None):
        
        url = self._make_url('/topup/stash')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'currencyCode': currency_code,
            'amount': amount,
            'metadata': metadata
        }
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def bank_checkout(self, product_name, currency_code, amount, bank_account, narration, metadata={}, callback=None):

        if narration is None:
            raise ValueError('Invalid narration')

        bank_account_schema = Schema({
            'accountNumber': And(str, len),
            'bankCode': And(int, lambda i: i in PaymentService.BANK.values()),
            Optional('accountName'): And(str, len),
            Optional('dateOfBirth'): And(str, lambda date: re.match('(\d{4})-(\d{2})-(\d{2})$', date))
        })
        bank_account = bank_account_schema.validate(bank_account)
        url = self._make_url('/bank/checkout/charge')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'bankAccount': bank_account,
            'currencyCode': currency_code,
            'amount': amount,
            'narration': str(narration),
            'metadata': metadata,
        }
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def __validate_checkout(self, checkout_type, transaction_id, otp, callback=None):

        assert checkout_type in ('bank', 'card')

        url = self._make_url('/' + checkout_type + '/checkout/validate')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'transactionId': str(transaction_id),
            'otp': str(otp),
        }
        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def validate_bank_checkout(self, transaction_id, otp, callback=None):
        return self.__validate_checkout('bank', transaction_id, otp, callback)

    def validate_card_checkout(self, transaction_id, otp, callback=None):
        return self.__validate_checkout('card', transaction_id, otp, callback)

    def card_checkout(self, product_name, currency_code, amount, narration,
                      payment_card=None, checkout_token=None, metadata={}, callback=None):

        if narration is None:
            raise ValueError('Invalid narration')

        if payment_card is None and checkout_token is None:
            raise ValueError('You need to provide either checkout_token or payment_card')

        countries = ('NG')
        url = self._make_url('/card/checkout/charge')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        data = {
            'username': self._username,
            'productName': product_name,
            'currencyCode': currency_code,
            'amount': amount,
            'narration': str(narration),
            'metadata': metadata,
        }

        if payment_card is not None:
            payment_card_schema = Schema({
                'number': And(str, len),
                'countryCode': And(str, lambda i: i in countries),
                'cvvNumber': And(int),
                'expiryMonth': And(int, lambda i: 1 <= i <= 12),
                'expiryYear': And(int, lambda i: i >= 2018),
                'authToken': And(str, len),
            })
            payment_card = payment_card_schema.validate(payment_card)
            data['paymentCard'] = payment_card
        else:
            data['checkoutToken'] = checkout_token

        data = json.dumps(data)
        return self._make_request(url, 'POST', headers=headers, params=None, data=data, callback=callback)

    def product_transactions(self, product_name, filters = {}, callback=None):
        
        url = self._make_url('/query/transaction/fetch')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        filters['username'] = self._username
        filters['productName'] = product_name
        if ('pageNumber' not in filters) or (filters['pageNumber'] is None):
            filters['pageNumber'] = "1"
        if ('count' not in filters) or (filters['count'] is None):
            filters['count'] = "100"
        return self._make_request(url, 'GET', headers=headers, params=filters, data=None, callback=callback)

    def find_transaction(self, transaction_id=None, callback=None):
        url = self._make_url('/query/transaction/find')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        if transaction_id is None:
            raise ValueError('Specify a transaction id.')
        params = {
            'username': self._username,
            'transactionId': transaction_id
        }
        return self._make_request(url, 'GET', headers=headers, params=params, data=None, callback=callback)

    def wallet_transactions(self, filters = {}, callback=None):

        url = self._make_url('/query/wallet/fetch')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        filters['username'] = self._username
        if ('pageNumber' not in filters) or (filters['pageNumber'] is None):
            filters['pageNumber'] = "1"
        if ('count' not in filters) or (filters['count'] is None):
            filters['count'] = "100"
        return self._make_request(url, 'GET', headers=headers, params=filters, data=None, callback=callback)

    def wallet_balance(self, callback=None):
        url = self._make_url('/query/wallet/balance')
        headers = dict(self._headers)
        headers['Content-Type'] = 'application/json'
        params = {
            'username': self._username
        }
        return self._make_request(url, 'GET', headers=headers, params=params, data=None, callback=callback)
        
