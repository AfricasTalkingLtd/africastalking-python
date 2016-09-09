"""
 COPYRIGHT (C) 2014 AFRICASTALKING LTD <www.africastalking.com>                                                   #

 AFRICAStALKING SMS GATEWAY CLASS IS A FREE SOFTWARE IE. CAN BE MODIFIED AND/OR REDISTRIBUTED
 UNDER THER TERMS OF GNU GENERAL PUBLIC LICENCES AS PUBLISHED BY THE
 FREE SOFTWARE FOUNDATION VERSION 3 OR ANY LATER VERSION

 THE CLASS IS DISTRIBUTED ON 'AS IS' BASIS WITHOUT ANY WARRANTY, INCLUDING BUT NOT LIMITED TO
 THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
 OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
PY_MAJOR_VERSION = sys.version_info[0]

if PY_MAJOR_VERSION < 3:
    from urllib import urlencode as urllib_urlencode
    import urllib2 as urllib_request
else:
    import urllib.request as urllib_request
    from urllib.parse import urlencode as urllib_urlencode

import json


class AfricasTalkingGatewayException(Exception):
    pass


class AfricasTalkingGateway:

    def __init__(self, username_, apiKey_):
        self.username = username_
        self.apiKey = apiKey_

        self.SMSURLString = "https://api.africastalking.com/version1/messaging"
        self.VoiceURLString = "https://voice.africastalking.com"
        self.SubscriptionURLString = "https://api.africastalking.com/version1/subscription"
        self.UserDataURLString = "https://api.africastalking.com/version1/user"
        self.AirtimeUrlString = "https://api.africastalking.com/version1/airtime"

        self.headers = {'Accept':
                        'application/json', 'apikey': apiKey_}

        self.HTTP_RESPONSE_OK = 200
        self.HTTP_RESPONSE_CREATED = 201

        # Turn this on if you run into problems. It will print the raw HTTP response from our server
        self.Debug = False

    # Messaging methods
    def sendMessage(self, to_, message_, from_=None, bulkSMSMode_=1, enqueue_=0, keyword_=None, linkId_=None, retryDurationInHours_=None):
        if len(to_) == 0 or len(message_) == 0:
            raise AfricasTalkingGatewayException(
                "Please provide both to_ and message_ parameters")

        parameters = {'username': self.username,
                      'to': to_,
                      'message': message_,
                      'bulkSMSMode': bulkSMSMode_}

        if not from_ is None:
            parameters["from"] = from_

        if enqueue_ > 0:
            parameters["enqueue"] = enqueue_

        if not keyword_ is None:
            parameters["keyword"] = keyword_

        if not linkId_ is None:
            parameters["linkId"] = linkId_

        if not retryDurationInHours_ is None:
            parameters["retryDurationInHours"] = retryDurationInHours_

        response = self.sendRequest(self.SMSURLString, parameters)

        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded['SMSMessageData']['Recipients']
        raise AfricasTalkingGatewayException(response)

    def fetchMessages(self, lastReceivedId_=0):
        url = "%s?username=%s&lastReceivedId=%s" % (
            self.SMSURLString, self.username, lastReceivedId_)

        response = self.sendRequest(url)

        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(response)
            return decoded['SMSMessageData']['Messages']
        raise AfricasTalkingGatewayException(response)

    # Subscription methods
    def createSubscription(self, phoneNumber_, shortCode_, keyword_):
        if len(phoneNumber_) == 0 or len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException(
                "Please supply phone number, short code and keyword")

        url = "%s/create" % (self.SubscriptionURLString)
        parameters = {
            'username': self.username,
            'phoneNumber': phoneNumber_,
            'shortCode': shortCode_,
            'keyword': keyword_
        }

        response = self.sendRequest(url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)

    def deleteSubscription(self, phoneNumber_, shortCode_, keyword_):
        if len(phoneNumber_) == 0 or len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException(
                "Please supply phone number, short code and keyword")

        url = "%s/delete" % (self.SubscriptionURLString)
        parameters = {
            'username': self.username,
            'phoneNumber': phoneNumber_,
            'shortCode': shortCode_,
            'keyword': keyword_
        }
        response = self.sendRequest(url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)

    def fetchPremiumSubscriptions(self, shortCode_, keyword_, lastReceivedId_=0):
        if len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException(
                "Please supply the short code and keyword")

        url = "%s?username=%s&shortCode=%s&keyword=%s&lastReceivedId=%s" % (self.SubscriptionURLString, self.username, shortCode_, keyword_, lastReceivedId_)

        result = self.sendRequest(url)
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(result)
            return decoded['responses']
        raise AfricasTalkingGatewayException(result)

    # Voice methods
    def call(self, from_, to_):
        parameters = {
            'username': self.username,
            'from': from_, 'to': to_
        }
        url = "%s/call" % (self.VoiceURLString)

        response = self.sendRequest(url, parameters)
        decoded = json.loads(response)
        if decoded['Status'] != "Success":
            raise AfricasTalkingGatewayException(decoded['ErrorMessage'])

    def getNumQueuedCalls(self, phoneNumber_, queueName_=None):
        parameters = {
            'username': self.username,
            'phoneNumbers': phoneNumber_
        }

        if queueName_ is not None:
            parameters['queueName'] = queueName_

        url = "%s/queueStatus" % (self.VoiceURLString)

        response = self.sendRequest(url, parameters)
        decoded = json.loads(response)
        if decoded['Status'] == "Success":
            return decoded['NumQueued']
        raise AfricasTalkingGatewayException(decoded['ErrorMessage'])

    def uploadMediaFile(self, urlString_):
        parameters = {
            'username': self.username,
            'url': urlString_
        }

        url = "%s/mediaUpload" % (self.VoiceURLString)

        response = self.sendRequest(url, parameters)
        decoded = json.loads(response)
        if decoded['Status'] != "Success":
            raise AfricasTalkingGatewayException(decoded['ErrorMessage'])

    #Airtime method
    def sendAirtime(self, recipients_):
        parameters = {
            'username': self.username,
            'recipients': json.dumps(recipients_)
        }

        SendAirtimeUrlString = "%s/send" % (self.AirtimeUrlString)

        response = self.sendRequest(SendAirtimeUrlString, parameters)
        decoded = json.loads(response)
        responses = decoded['responses']
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            if len(responses) > 0:
                return responses
            raise AfricasTalkingGatewayException(decoded["errorMessage"])
        raise AfricasTalkingGatewayException(response)

    # Userdata method
    def getUserData(self):
        url = "%s?username=%s" % (self.UserDataURLString, self.username)
        result = self.sendRequest(url)
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(result)
            return decoded['UserData']
        raise AfricasTalkingGatewayException(result)

    # HTTP access method
    def sendRequest(self, urlString, data_=None):
        try:
            if data_ is not None:
                data = urllib_urlencode(data_)
                request = urllib_request.Request(
                    urlString, data, headers=self.headers)
            else:
                request = urllib_request.Request(urlString, headers=self.headers)

            response = urllib_request.urlopen(request)
        except Exception as e:
            raise AfricasTalkingGatewayException(str(e))
        else:
            self.responseCode = response.getcode()
            response = response.read().decode('utf-8')
            if self.Debug:
                print(response)
            return response
