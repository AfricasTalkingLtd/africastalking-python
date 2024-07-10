from .Token import TokenService
from .Application import ApplicationService
from .Airtime import AirtimeService
from .SMS import SMSService
from .Voice import VoiceService
from .MobileData import MobileDataService
from .Insights import InsightService

SMS = None
Airtime = None
USSD = None
Voice = None
Application = None
Token = None
MobileData = None
Insights = None


def initialize(username, api_key):
    if username is None or api_key is None:
        raise RuntimeError("Invalid username and/or api_key")

    globals()["SMS"] = SMSService(username, api_key)
    globals()["Airtime"] = AirtimeService(username, api_key)
    globals()["Voice"] = VoiceService(username, api_key)
    globals()["Application"] = ApplicationService(username, api_key)
    globals()["Token"] = TokenService(username, api_key)
    globals()["MobileData"] = MobileDataService(username, api_key)
    globals()["Insights"] = InsightService(username, api_key)
    # globals()['USSD'] = USSDService(username, api_key)
