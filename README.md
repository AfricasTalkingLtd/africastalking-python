# africastalking-python
Official AfricasTalking Python API wrapper

A Python library for communicating with the AfricasTalking REST API. Need help? Post your questions to support@africastalking.com

#### Installing
```bash
$ pip install AfricastalkingGateway
```

#### Note

The gateway package belongs to module ```africastalking```, import as:

```python
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
```


#### Sending a message

```python
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)

# Specify your login credentials
username = "MyAfricasTalkingUsername"
apikey   = "MyAfricasTalkingAPIKey"

# Please ensure you include the country code (+254 for Kenya in this case)
to      = "+254711XXXYYY,+254733YYYZZZ"

message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"

# Create a new instance of our awesome gateway class
gateway = AfricasTalkingGateway(username, apikey)

try:
    # Thats it, hit send and we'll take care of the rest.
    
    results = gateway.sendMessage(to, message)

    for recipient in results:
        # status is either "Success" or "error message"
        print 'number=%s;status=%s;messageId=%s;cost=%s' %(recipient['number'],
                                                        recipient['status'],
                                                        recipient['messageId'],
                                                        recipient['cost'])
except AfricasTalkingGatewayException, e:
    print 'Encountered an error while sending: %s' % str(e)
```

#### Fetching messages (via a callback url)
(Sample code in Flask. Django is not too different, POST params within the request object)

- Add a callback URL on the accounts page

```python
# define a method/ endpoint/ route to receive the POST params we send to you:

@app.route('/api/sms/dlr/', methods=['POST'])
def dlr_callback():
        # Reads the variables sent via POST from our gateway
        _from = request.values.get('from', None)
        to = request.values.get('to', None)
        text = request.values.get('text', None)
        date = request.values.get('date', None)
        id_ = request.values.get('id', None)

        try:
            # update db or some sort of operation
            logging.info(_from, to, text, date, id_)

        except Exception as e:
            logging.error('Failed with - ', e)

        resp = make_response('Ok', 200)
        resp.headers['Content-Type'] = 'text/plain'
        resp.cache_control.no_cache = True
        return resp
```

#### Fetching messages (via fetch messages)

```python
try:
    # Our gateway will return 10 messages at a time back to you, starting with
    # what you currently believe is the lastReceivedId. Specify 0 for the first
    # time you access the gateway, and the ID of the last message we sent you
    # on subsequent results
    lastReceivedId = 0;
    
    while True:
        messages = gateway.fetchMessages(lastReceivedId)
        
        for message in messages:
            print 'from=%s;to=%s;date=%s;text=%s;linkId=%s;' %(message['from'],
                                                            message['to'],
                                                            message['date'],
                                                            message['text'],
                                                            message['linKId'])
            lastReceivedId = message['id']
    if len(messages) == 0:
        break

except AfricasTalkingGatewayException, e:
    print 'Encountered an error while fetching messages: %s' % str(e)
```


#### Voice - Making a call

```python
# create an instance of the AT gateway class
# define apikey and username
# Specify your Africa's Talking phone number in international format
callFrom = "+254711082XYZ"

# Specify the numbers that you want to call to in a comma-separated list
# Please ensure you include the country code (+254 for Kenya in this case, +256 Uganda)
callTo   = "+254711XXXYYY,+254733YYYZZZ"

# Create a new instance of our awesome gateway class
gateway  = AfricasTalkingGateway(username, apikey)

try:
    # Make the call
    results = gateway.call(callFrom, callTo)
    
    for result in results:
        # Only status "Queued" means the call was successfully placed
        print "Status : %s; phoneNumber : %s " % (result['status'], 
                                result['phoneNumber'])
    
    # Our API will now contact your callback URL once recipient answers the call!
except AfricasTalkingGatewayException, e:
    print 'Encountered an error while making the call: %s' % str(e)
```

#### Sending Airtime 

```python
# Specify an array of dicts to hold the recipients and the amount to send
recipients = [{"phoneNumber" : "+2547XXYYYZZZ", 
               "amount"      : "KES XX"}]

# Create a new instance of our awesome gateway class
gateway    = AfricasTalkingGateway(username, apikey)

try:
    # Thats it, hit send and we'll take care of the rest. 
    responses = gateway.sendAirtime(recipients)
    for response in responses:
        print "phoneNumber=%s; amount=%s; status=%s; discount=%s; requestId=%s" %(response['phoneNumber'],
                        response['amount'],
                        response['status'],
                        response['discount']
                        response['requestId'])

except AfricasTalkingGatewayException, e:
    print 'Encountered an error while sending airtime: %s' % str(e)
```

#### Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.

2. Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).

3. Write a test which shows that the bug was fixed or that the feature works as expected.

4. Send a pull request and bug the maintainer until it gets merged and published. :)
