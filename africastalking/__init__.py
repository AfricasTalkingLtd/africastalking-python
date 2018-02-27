from Service import AfricasTalkingException

from Token import TokenService
from Account import AccountService
from Airtime import AirtimeService
from SMS import SmsService
from Payment import PaymentService

__SERVICE_SMS = 'sms'
__SERVICE_AIRTIME = 'airtime'
__SERVICE_PAYMENT = 'payment'
__SERVICE_VOICE = 'voice'
__SERVICE_USSD = 'ussd'
__SERVICE_TOKEN = 'token'
__SERVICE_ACCOUNT = 'account'

__USERNAME = None
__API_KEY = None


def initialize(username, api_key):
    globals()['__USERNAME'] = username
    globals()['__API_KEY'] = api_key


def get_sms_service():
    return __get_service(__SERVICE_SMS)


def get_airtime_service():
    return __get_service(__SERVICE_AIRTIME)


def get_payment_service():
    return __get_service(__SERVICE_PAYMENT)


def get_voice_service():
    return __get_service(__SERVICE_VOICE)


def get_ussd_service():
    return __get_service(__SERVICE_USSD)


def get_account_service():
    return __get_service(__SERVICE_ACCOUNT)


def get_token_service():
    return __get_service(__SERVICE_TOKEN)


def __get_service(service):
    if __USERNAME is None or __API_KEY is None:
        raise RuntimeError('You need to call africastalking.initialize() first')

    if service == __SERVICE_SMS:
        return SmsService(__USERNAME, __API_KEY)
    elif service == __SERVICE_AIRTIME:
        return AirtimeService(__USERNAME, __API_KEY)
    elif service == __SERVICE_PAYMENT:
        return PaymentService(__USERNAME, __API_KEY)
    elif service == __SERVICE_VOICE:
        pass
    elif service == __SERVICE_USSD:
        pass
    elif service == __SERVICE_TOKEN:
        return TokenService(__USERNAME, __API_KEY)
    elif service == __SERVICE_ACCOUNT:
        return AccountService(__USERNAME, __API_KEY)
    else:
        raise AfricasTalkingException('Unknown service: ' + service)
