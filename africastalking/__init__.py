from Service import AfricasTalkingException

from Token import TokenService
from Account import AccountService
from Airtime import AirtimeService

SERVICE_SMS = 'sms'
SERVICE_AIRTIME = 'airtime'
SERVICE_PAYMENT = 'payment'
SERVICE_VOICE = 'voice'
SERVICE_USSD = 'ussd'
SERVICE_TOKEN = 'token'
SERVICE_ACCOUNT = 'account'

__USERNAME = None
__API_KEY = None


def initialize(username, api_key):
    globals()['__USERNAME'] = username
    globals()['__API_KEY'] = api_key


def get_service(service):
    if __USERNAME is None or __API_KEY is None:
        raise RuntimeError('You need to call africastalking.initialize() first')

    if service == SERVICE_SMS:
        pass
    elif service == SERVICE_AIRTIME:
        return AirtimeService(__USERNAME, __API_KEY)
    elif service == SERVICE_PAYMENT:
        pass
    elif service == SERVICE_VOICE:
        pass
    elif service == SERVICE_USSD:
        pass
    elif service == SERVICE_TOKEN:
        return TokenService(__USERNAME, __API_KEY)
    elif service == SERVICE_ACCOUNT:
        return AccountService(__USERNAME, __API_KEY)
    else:
        raise AfricasTalkingException('Unknown service: ' + service)
