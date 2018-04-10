# africastalking-python

![](https://img.shields.io/pypi/v/africastalking.svg)

> The SDK provides convenient access to the Africa's Talking APIs to python apps.


## Documentation
Take a look at the [API docs here](http://docs.africastalking.com).

## Install

```bash
$ pip  install africastalking # python 2.7.x

OR

$ python -m pip install africastalking # python 2.7.x

OR

$ pip3 install africastalking # python 3.6.x

OR

$ python3 -m pip install africastalking # python 3.6.x

```


## Usage

The package needs to be configured with your app username and API key, which you can get from the [dashboard](https://account/africastalking.com).

> You can use this SDK for either production or sandbox apps. For sandbox, the app username is **ALWAYS** `sandbox`

```python
# import package
import africastalking


# Initialize SDK
username = "YOUR_USERNAME"    # use 'sandbox' for development in the test environment
api_key = "YOUR_API_KEY"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("Hello Message!", ["+2547xxxxxx"])
print(response)

# Or use it asynchronously
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)

sms.send("Hello Message!", ["+2547xxxxxx"], callback=on_finish)    

```

See [example](example/) for more usage examples.


## Initialization

Initialize the SDK by calling `africastalking.initialize(username, api_key)`. After initialization, you can get instances of offered services as follows:

- [Application](#applicationservice): `africastalking.Application`
- [Airtime](#airtimeservice): `africastalking.Airtime`
- [SMS](#smsservice): `africastalking.SMS`
- [Payments](#paymentservice): `africastalking.Payments`
- [Voice](#voiceservice): `africastalking.Voice`
- [Token](#tokenservice): `africastalking.Token`
- [USSD](#ussdservice): `africastalking.USSD`

## Services

All methods are synchronous (i.e. will block current thread) but provide asynchronous variants that take a callback `function (error: AfricasTalkingException, data: dict)`.

The synchronous variant always return and instance a `dict` while the async one returns a `Thread`.

All phone numbers use the international format. e.g. `+234xxxxxxxx`.

All **amount strings** contain currency code as well. e.g. `UGX 443.88`.

### `ApplicationService`

- `fetch_application_data()`: Get app balance info.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
application = africastalking.Application
res = application.fetch_application_data()
```

### `AirtimeService`

- `send(phone_number: str, amount: str)`: Send airtime to a phone number. An example amount would be `KES 150`.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
airtime = africastalking.Airtime
res = airtime.send(phone_number='+254718769882', amount='KES 908')
```

- `send(recipients: [dict])`: Send airtime to a list of phone numbers. The keys in the `recipients` dictionary are phone numbers while the values are airtime amounts. The amounts need to have currency info e.g. `UXG 4265`.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
airtime = africastalking.Airtime
res = airtime.send(recipients=[
            {'phoneNumber': '+2348160663047', 'amount': 'NGN 1535' },
            {'phoneNumber': '+254718769881', 'amount': 'KES 733'},
])
```

For more information about status notification, please read [http://docs.africastalking.com/airtime/callback](http://docs.africastalking.com/airtime/callback)


### `SmsService`

- `send(message: str, recipients: [str], sender_id: str = None, enqueue: bool = False)`: Send a bulk message to recipients, optionally from `sender_id` (Short Code or Alphanumeric).


```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
sms = africastalking.SMS
res = sms.send(message='hello', recipients=['+254718769882'])
```

- `send_premium(message: str, keyword: str, link_id: str, recipients: [str])`: Send a premium SMS


```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
sms = africastalking.SMS
res = sms.send_premium(message='hello', keyword='music', link_id='233dddd', recipients=['+254718769882'])
```

- `fetch_messages(last_received_id: int = 0)`: Fetch your messages

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
sms = africastalking.SMS
res = sms.fetch_messages()
```

- `fetch_subscriptions(short_code: str, keyword: str, last_received_id: int = 0)`: Fetch your premium subscription data


```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
sms = africastalking.SMS
res = sms.fetch_subscriptions(short_code='6673', keyword='music')
```

- `create_subscription(short_code: str, keyword: str, phone_number: str, checkout_token: str)`: Create a premium subscription

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
sms = africastalking.SMS
token = africastalking.Token
res = token.create_checkout_token(phone_number='+254718767882')
checkout_token = res['token']
res = sms.create_subscription(short_code='6673', keyword='music', phone_number='+254718767882', checkout_token=checkout_token)
```

- `delete_subscription(short_code: str, keyword: str, phone_number: str)`: Delete a premium subscription

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
sms = africastalking.SMS
res = sms.delete_subscription(short_code='6673', keyword='music', phone_number='+254718767882')
```



For more information on: 

- How to receive SMS: [http://docs.africastalking.com/sms/callback](http://docs.africastalking.com/sms/callback)
- How to get notified of delivery reports: [http://docs.africastalking.com/sms/deliveryreports](http://docs.africastalking.com/sms/deliveryreports)
- How to listen for subscription notifications: [http://docs.africastalking.com/subscriptions/callback](http://docs.africastalking.com/subscriptions/callback)

### `PaymentService`

- `card_checkout(product_name: str, currency_code:str, amount: float, payment_card: dict, narration: str, metadata: dict = {})`: Initiate card checkout.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
card = {
    'number': '3234324235452345',
    'countryCode': 'NG',
    'cvvNumber': 3343,
    'expiryMonth': 3, # 1-12
    'expiryYear': 2022, # > 2018
    'authToken': '3322' # card pin
}
res = payment.card_checkout(product_name='TestProduct', currency_code='NGN', amount=7822, payment_card=card, narration='Small Chops Checkout')
```

- `validate_card_checkout(transaction_id: str, otp: str)`: Validate a card checkout

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.validate_card_checkout(transaction_id='ATId_3829u49283u423u', otp='233333')
```

- `bank_checkout(product_name: str, currency_code: str, amount: float, bank_account: dict, narration: str, metadata: dict = {})`: Initiate bank checkout.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
account = {
    'accountNumber': '3234324235452345',
    'bankCode': payment.BANK['FCMB_NG'],
    'accountName': 'Fake Bob Naija',
    # Optional YYYY-MM-DD // required only for Zenith Nigeria
    #'dateOfBirth': '2000-01-01'
}
res = payment.bank_checkout(product_name='TestProduct', currency_code='NGN', amount=7822, bank_account=account, narration='Small Chops Checkout')
```

- `validate_bank_checkout(transaction_id: str, otp: str)`: Validate a bank checkout


```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.validate_bank_checkout(transaction_id='ATId_3829u492SQSW383u423u', otp='AA22w33')
```

- `bank_transfer(product_name: str, recipients: [dict])`: Move money form payment wallet to bank account.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
recipients = [
    {
      "bankAccount": {
        "accountNumber": "3234324235452345",
        "bankCode": payment.BANK['FCMB_NG'],
        "accountName": "Fake Bob Naija"
      },
      "currencyCode": "NGN",
      "amount": 332434,
      "narration": "Some description",
      "metadata": {}
    }
]
res = payment.bank_transfer(product_name='TestProduct', recipients=recipients)
```

- `wallet_transfer(product_name: str, target_product_code: int, currency_code: str, amount: float, metadata: dict)`: Transfer money from one Payment Product to another Payment Product hosted on Africa's Talking.

.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.wallet_transfer(product_name='TestProduct', target_product_code=2009, currency_code='KES', amount=7732, metadata={'ID': '23GG')
```

- `topup_stash(product_name: str, currency_code: str, amount: float, metadata: dict)`: Move money from a Payment Product to an app's stash.

.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.topup_stash(product_name='TestProduct', currency_code='KES', amount=7732, metadata={'ID': '23GG')
```

- `mobile_checkout(product_name: str, phone_number: str, currency_code: str, amount: float, metadata: dict = {})`: Initiate mobile checkout. An example amount would be `KES 323`

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.mobile_checkout(product_name='TestProduct', currency_code='KES', amount=565)
```

- `mobile_b2c(product_name: str, consumers: [dict])`: Send mobile money to consumer. Each consumer is a `dict` of this format:


```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
consumers = [
    {
    
      "name": "Bob Mwangi",
      "phoneNumber": "+254718769882",
      "currencyCode": "KES",
      "amount": 6766.88,
      "providerChannel": "1212",
      "reason": 'SalaryPayment',
      "metadata": {}
    }
]
res = payment.mobile_b2c(product_name='TestProduct', consumers=consumers)
```

- `mobile_b2b(product_name: str, business: dict)`: Send mobile money to business.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
business = {
  "currencyCode": "KES",
  "amount": 6766.88,
  "destinationChannel": "1212",
  "destinationAccount": "ABC",
  "provider": 'Mpesa',
  "transferType": 'BusinessBuyGoods',
  "metadata": {}
}
res = payment.mobile_b2b(product_name='TestProduct', business=business)
```


For more information, please read [http://docs.africastalking.com/payments](http://docs.africastalking.com/payments)

### `VoiceService`

- `call(source: str, destination: str)`: Initiate a phone call

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
voice = africastalking.Voice
res = voice.call(source="+254718769881", destination="+254718769880")
```

- `fetch_queued_calls(phone_number: str)`: Get queued calls

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
voice = africastalking.Voice
res = voice.fetch_queued_calls(phone_number="+2548933373")
```

- `upload_media_file(phone_number: str, url: str)`: Upload voice media file

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
voice = africastalking.Voice
res = voice.upload_media_file(phone_number="+2548933373", url="https://www.my-site.zr/my_fil.mp3")
```


For more information, please read [http://docs.africastalking.com/voice](http://docs.africastalking.com/voice)


### `TokenService`

- `create_checkout_token(phone_number: str)`: Create a new checkout token for `phone_number`.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
token = africastalking.Token
res = token.create_checkout_token("+254787633677")
```

- `generate_auth_token()`: Generate an auth token to use for authentication instead of an API key.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
token = africastalking.Token
res = token.generate_auth_token()
```

### `UssdService`

For more information, please read [http://docs.africastalking.com/ussd](http://docs.africastalking.com/ussd)


## Development
```shell
$ git clone https://github.com/AfricasTalkingLtd/africastalking-python.git
$ cd africastalking-python
$ touch .env
```

Make sure your `.env` file has the following content then run `python -m unittest discover -v`

```ini
# AT API
USERNAME=sandbox
API_KEY=some_key
```

## Issues

If you find a bug, please file an issue on [our issue tracker on GitHub](https://github.com/AfricasTalkingLtd/africastalking-python/issues).
