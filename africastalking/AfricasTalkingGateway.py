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

import json
import requests # urllib please - we're done


class AfricasTalkingGatewayException(Exception):
    pass

class AfricasTalkingGateway:

    def __init__(self, username, apiKey, environment = 'production'):
        self.username    = username
        self.apiKey      = apiKey
        self.environment = environment
 
        self.HTTP_RESPONSE_OK       = 200
        self.HTTP_RESPONSE_CREATED  = 201
 
        # Turn this on if you run into problems. It will print the raw HTTP response from our server
        self.Debug                  = False

    # Messaging methods
    def sendMessage(self, to_, message_, from_ = None, bulkSMSMode_ = 1, enqueue_ = 0, keyword_ = None, linkId_ = None, retryDurationInHours_ = None):
        if len(to_) == 0 or len(message_) == 0:
            raise AfricasTalkingGatewayException("Please provide both to_ and message_ parameters")
        
        parameters = {'username' : self.username,
                      'to': to_,
                      'message': message_,
                      'bulkSMSMode':bulkSMSMode_}
        
        if not from_ is None :
            parameters["from"] = from_

        if enqueue_ > 0:
            parameters["enqueue"] = enqueue_

        if not keyword_ is None:
            parameters["keyword"] = keyword_
            
        if not linkId_ is None:
            parameters["linkId"] = linkId_

        if not retryDurationInHours_ is None:
            parameters["retryDurationInHours"] =  retryDurationInHours_

        response = self.sendRequest(self.getSmsUrl(), parameters)
        
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            recipients = decoded['SMSMessageData']['Recipients']
            
            if len(recipients) > 0:
                return recipients
                
            raise AfricasTalkingGatewayException(decoded['SMSMessageData']['Message'])
 
        raise AfricasTalkingGatewayException(response)


    def fetchMessages(self, lastReceivedId_ = 0):
        url = "%s?username=%s&lastReceivedId=%s" % (self.getSmsUrl(), self.username, lastReceivedId_)
        response = self.sendRequest(url)
        
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(response)
            return decoded['SMSMessageData']['Messages']
        raise AfricasTalkingGatewayException(response)


    # Subscription methods
    def createSubscription(self, phoneNumber_, shortCode_, keyword_):
        if len(phoneNumber_) == 0 or len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException("Please supply phone number, short code and keyword")
        
        url        = "%s/create" %(self.getSmsSubscriptionUrl())
        parameters = {
            'username'    :self.username,
            'phoneNumber' :phoneNumber_,
            'shortCode'   :shortCode_,
            'keyword'     :keyword_
            }
        
        response = self.sendRequest (url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)

        
    def deleteSubscription(self, phoneNumber_, shortCode_, keyword_):
        if len(phoneNumber_) == 0 or len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException("Please supply phone number, short code and keyword")
        
        url        = "%s/delete" %(self.getSmsSubscriptionUrl())
        parameters = {
            'username'     :self.username,
            'phoneNumber'  :phoneNumber_,
            'shortCode'    :shortCode_,
            'keyword'      :keyword_
            }
        response = self.sendRequest(url, parameters)
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)

    
    def fetchPremiumSubscriptions(self,shortCode_, keyword_, lastReceivedId_ = 0):
        if len(shortCode_) == 0 or len(keyword_) == 0:
            raise AfricasTalkingGatewayException("Please supply the short code and keyword")
        
        url    = "%s?username=%s&shortCode=%s&keyword=%s&lastReceivedId=%s" % (self.getSmsSubscriptionUrl(),
                                                                               self.username,
                                                                               shortCode_,
                                                                               keyword_,
                                                                               lastReceivedId_)
        result = self.sendRequest(url)
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(result)
            return decoded['responses']
        
        raise AfricasTalkingGatewayException(response)


    # Voice methods
    def call(self, from_, to_):
        parameters = {
            'username' : self.username,
            'from'     : from_,
            'to': to_ 
            }
        
        url      = "%s/call" %(self.getVoiceUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        if decoded['errorMessage'] == "None":
            return decoded['entries'];
        raise AfricasTalkingGatewayException(decoded['errorMessage'])
        
    def getNumQueuedCalls(self, phoneNumber_, queueName_ = None):
        parameters = {
            'username'    :self.username,
            'phoneNumbers' :phoneNumber_
            }
        
        if queueName_ is not None:
            parameters['queueName'] = queueName_
            
        url      = "%s/queueStatus" %(self.getVoiceUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        if decoded['errorMessage'] == "None":
            return decoded['entries']
        
        raise AfricasTalkingGatewayException(decoded['errorMessage'])
        
    def uploadMediaFile(self, urlString_):
        parameters = {
            'username' :self.username, 
            'url'      :urlString_
            }
        url      = "%s/mediaUpload" %(self.getVoiceUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        if decoded['errorMessage'] != "None":
            raise AfricasTalkingGatewayException(decoded['errorMessage'])

    #Airtime method
    def sendAirtime(self, recipients_):
        parameters = {
            'username'   : self.username,
            'recipients' : json.dumps(recipients_) 
            }
        
        url      = "%s/send" %(self.getAirtimeUrl())
        response = self.sendRequest(url, parameters)
        decoded  = json.loads(response)
        responses = decoded['responses']
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            if len(responses) > 0:
                return responses
            raise AfricasTalkingGatewayException(decoded["errorMessage"])
        raise AfricasTalkingGatewayException(response)

    #Payment Methods
    def initiateMobilePaymentCheckout(self,
                                      productName_,
                                      phoneNumber_,
                                      currencyCode_,
                                      amount_,
                                      metadata_):
        parameters = {
            'username'     : self.username,
            'productName'  : productName_,
            'phoneNumber'  : phoneNumber_,
            'currencyCode' : currencyCode_,
            'amount'       : amount_,
            'metadata'     : metadata_
            }
        url      = self.getMobilePaymentCheckoutUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            if decoded['status'] == 'PendingConfirmation':
                return decoded['transactionId']
            raise AfricasTalkingGatewayException(decoded['description'])
        raise AfricasTalkingGatewayException(response)

    def mobilePaymentB2CRequest(self, productName_, recipients_):
        parameters = {
            'username'    : self.username,
            'productName' : productName_,
            'recipients'  : recipients_
            }
        url      = self.getMobilePaymentB2CUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            if len(decoded['entries']) > 0:
                return decoded['entries']
            raise AfricasTalkingGatewayException(decoded['errorMessage'])
        raise AfricasTalkingGatewayException(response)

    def mobilePaymentB2BRequest(self, productName_, providerData_, currencyCode_, amount_, metadata_):
        if "provider" not in providerData_:
            raise AfricasTalkingGatewayException("Missing field provider")
            
        if "destinationChannel" not in providerData_:
            raise AfricasTalkingGatewayException("Missing field destinationChannel")

        if "destinationAccount" not in providerData_:
            raise AfricasTalkingGatewayException("Missing field destinationAccount")
            
        if "transferType" not in providerData_:
            raise AfricasTalkingGatewayException("Missing field transferType")
            
        parameters = {
            'username'    : self.username,
            'productName' : productName_,
            'provider' : providerData_['provider'],
            'destinationChannel'  : providerData_['destinationChannel'],
            'destinationAccount': providerData_['destinationAccount'],
            'transferType'  : providerData_['transferType'],
            'currencyCode' : currencyCode_,
            'amount' : amount_,
            'metadata' : metadata_
            }
            
        url      = self.getMobilePaymentB2BUrl()
        response = self.sendJSONRequest(url, json.dumps(parameters))
        if self.responseCode == self.HTTP_RESPONSE_CREATED:
            decoded = json.loads(response)
            return decoded
        raise AfricasTalkingGatewayException(response)
        
        
    # Userdata method
    def getUserData(self):
        url    = "%s?username=%s" %(self.getUserDataUrl(), self.username)
        result = self.sendRequest(url)
        if self.responseCode == self.HTTP_RESPONSE_OK:
            decoded = json.loads(result)
            return decoded['UserData']
        raise AfricasTalkingGatewayException(response)

    # HTTP access method
    def sendRequest(self, urlString, data_ = None):
        try:
            headers = { 'Accept' : 'application/json',
                       'apikey' : self.apiKey }

            if data_ is not None:
                resp = requests.post(urlString, data=data_, headers=headers)
            else:
                resp = requests.post(urlString, headers=headers)

        except requests.exceptions.Timeout as e:
            raise AfricasTalkingGatewayException(e.read())

        except requests.exceptions.RequestException as e:
            raise AfricasTalkingGatewayException(e.read())
 
        else:
            self.responseCode = resp.status_code

            response          = resp.text
            if self.Debug:
                print("Raw response: " + response)
 
            return response

    def sendJSONRequest(self, urlString, data_):
        try:
            headers  = { 'Accept'       : 'application/json',
                         'Content-Type' : 'application/json',
                         'apikey'       : self.apiKey }

            resp = requests.post(urlString, data = data_, headers = headers)

        except requests.exceptions.Timeout as e:
            raise AfricasTalkingGatewayException(e.read())

        except requests.exceptions.RequestException as e:
            raise AfricasTalkingGatewayException(e.read())
 
        else:
            self.responseCode = resp.status_code
            response          = resp.text
            if self.Debug:
                print("Raw response: " + response)
 
            return response

    def getApiHost(self):
        if self.environment == 'sandbox':
            return 'https://api.sandbox.africastalking.com'
        else:
            return 'https://api.africastalking.com'

    def getVoiceHost(self):
        if self.environment == 'sandbox':
            return 'https://voice.sandbox.africastalking.com'
        else:
            return 'https://voice.africastalking.com'

    def getPaymentHost(self):
        if self.environment == 'sandbox':
            return 'https://payments.sandbox.africastalking.com'
        else:
            return 'https://payments.africastalking.com'
  
    def getSmsUrl(self):
        return self.getApiHost() + "/version1/messaging"

    def getVoiceUrl(self):
        return self.getVoiceHost()

    def getSmsSubscriptionUrl(self):
        return self.getApiHost() + "/version1/subscription"

    def getUserDataUrl(self):
        return self.getApiHost() + "/version1/user"

    def getAirtimeUrl(self):
        return self.getApiHost() + "/version1/airtime"

    def getMobilePaymentCheckoutUrl(self):
        return self.getPaymentHost() + "/mobile/checkout/request"

    def getMobilePaymentB2CUrl(self):
        return self.getPaymentHost() + "/mobile/b2c/request"

    def getMobilePaymentB2BUrl(self):
        return self.getPaymentHost() + "/mobile/b2b/request"
    
