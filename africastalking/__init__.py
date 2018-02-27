from Service import AfricasTalkingException

from Token import TokenService
from Account import AccountService
from Airtime import AirtimeService
from SMS import SMSService
from Payment import PaymentService

SMS = None
Airtime = None
Payment = None
# To avoid confusion
Payments = Payment
USSD = None
Voice = None
Account = None
Token = None


def initialize(username, api_key):

    if username is None or api_key is None:
        raise RuntimeError('Invalid username and/or api_key')

    globals()['SMS'] = SMSService(username, api_key)
    globals()['Airtime'] = AirtimeService(username, api_key)
    globals()['Payment'] = PaymentService(username, api_key)
    # globals()['Voice'] = VoiceService(username, api_key)
    globals()['Account'] = AccountService(username, api_key)
    globals()['Token'] = TokenService(username, api_key)
    # globals()['USSD'] = USSDService(username, api_key)

