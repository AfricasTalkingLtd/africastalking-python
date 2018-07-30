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

- [SMS](#sms): `africastalking.SMS`
- [Airtime](#airtime): `africastalking.Airtime`
- [Payments](#paymentservice): `africastalking.Payments`
- [Voice](#voiceservice): `africastalking.Voice`
- [Token](#tokenservice): `africastalking.Token`
- [Application](#application): `africastalking.Application`

### `Application`

- `fetch_application_data()`: Get app information. e.g balance.

### `Airtime`

- `send(recipients: [dict])`: Send airtime

    - `recipients`: Contains an array of arrays containing the following keys
            - `phoneNumber`: Recipient of airtime
            - `amount`: Amount to send with currency e.g `KES 100`
            
### `Sms`

- `send(message: str, recipients: [str], sender_id: str = None, enqueue: bool = False)`: Send a message.

    - `message`: SMS content. `REQUIRED`
    - `recipients`: An array of phone numbers. `REQUIRED`
    - `sender_id`: Shortcode or alphanumeric ID that is registered with your Africa's Talking account.
    - `enqueue`: Set to `true` if you would like to deliver as many messages to the API without waiting for an acknowledgement from telcos.

- `send_premium(message: str, keyword: str, link_id: str, recipients: [str])`: Send a premium SMS

    - `message`: SMS content. `REQUIRED`
    - `recipients`: An array of phone numbers. `REQUIRED`
    - `keyword`: Your premium product keyword `REQUIRED`
    - `link_id`: "[...] We forward the `linkId` to your application when a user sends a message to your onDemand service"
    - `retry_duration_in_hours`: "This specifies the number of hours your subscription message should be retried in case it's not delivered to the subscriber"

- `fetch_messages(last_received_id: int = 0)`: Fetch your messages

    - `last_received_id`: This is the id of the message you last processed. Defaults to `0`
    
- `create_subscription(short_code: str, keyword: str, phone_number: str, checkout_token: str)`: Create a premium subscription

    - `short_code`: Premium short code mapped to your account. `REQUIRED`
    - `keyword`: Premium keyword under the above short code and is also mapped to your account. `REQUIRED`
    - `phone_number`: PhoneNumber to be subscribed `REQUIRED`
    - `checkout_token`: Token used to validate the subscription request `REQUIRED`. See [token service](#token)

- `fetch_subscriptions(short_code: str, keyword: str, last_received_id: int = 0)`: Fetch your premium subscription data

    - `short_code`: Premium short code mapped to your account. `REQUIRED`
    - `keyword`: Premium keyword under the above short code and mapped to your account. `REQUIRED`
    - `last_received_id`: ID of the subscription you believe to be your last. Defaults to `0`

- `delete_subscription(short_code: str, keyword: str, phone_number: str)`: Delete a phone number from a premium subscription

    - `short_code`: Premium short code mapped to your account. `REQUIRED`
    - `keyword`: Premium keyword under the above short code and is also mapped to your account. `REQUIRED`
    - `phone_number`: PhoneNumber to be subscribed `REQUIRED`
    
    
### `PaymentService`

- `mobile_checkout(product_name: str, phone_number: str, currency_code: str, amount: float, metadata: dict = {})`: Charge a customers mobile money account

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `phone_number`: Customer phone number (in international format). `REQUIRED`
    - `currency_code`: 3-digit ISO format currency code (e.g `KES`, `USD`, `UGX` etc). `REQUIRED`
    - `amount`: Amount to charge. `REQUIRED`
    - `metadata`: Additional data to associate with the transaction. `REQUIRED`
    
- `mobile_b2c(product_name: str, consumers: [dict])`: Send mobile money to customers:

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `consumers`: A list of **up to 10** recipients. Each recipient has:

        - `phoneNumber`: Customer phone number (in international format). `REQUIRED`
        - `currencyCode`: 3-digit ISO format currency code (e.g `KES`, `USD`, `UGX` etc). `REQUIRED`
        - `amount`: Amount to pay. `REQUIRED`
        - `reason`: The purpose of the payment. See `payments::REASON*` for supported reasons. `REQUIRED`
        - `metadata`: Additional data to associate with the tranasction. `REQUIRED`

- `mobile_b2b(product_name: str, business: dict)`: Send mobile money to business.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `business`:  Business details
      - `provider`: Payment provider that is facilitating this transaction. See `payments::PROVIDER*` for supported providers. `REQUIRED`
      - `transferType`: Describes the type of payment being made. See `payments::TRANSFER_TYPE*` for supported transfer types. `REQUIRED`
      - `currencyCode`: 3-digit ISO format currency code (e.g `KES`, `USD`, `UGX` etc). `REQUIRED`
      - `destinationChannel`: Name or number of the channel that will receive payment by the provider. `REQUIRED`
      - `destinationAccount`: Name used by the business to receive money on the provided destinationChannel. `REQUIRED`
      - `amount`: Amount to pay. `REQUIRED`
      - `metadata`: Additional data to associate with the transaction. `REQUIRED`

- `bank_checkout(product_name: str, currency_code: str, amount: float, bank_account: dict, narration: str, metadata: dict = {})`: Initiate bank checkout.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `bank_account`: Bank account to be charged:

        - `accountName`: Name of the bank account. `REQUIRED`
        - `accountNumber`: Account number. `REQUIRED`
        - `bankCode`: A [6-Digit Integer Code](http://docs.africastalking.com/bank/checkout#bankCodes) for the bank that we allocate. See `payments::BANK*` for supported banks. `REQUIRED`
        - `dateOfBirth`: Date of birth of the account owner (in the format `YYYY-MM-DD`). Required for Zenith Bank Nigeria.

    - `currency_ode`: 3-digit ISO format currency code (only `NGN` is supported at present). `REQUIRED`
    - `amount`: Amount to charge. `REQUIRED`
    - `narration`: A short description of the transaction. `REQUIRED`
    - `metadata`: Additional data to associate with the transaction. `REQUIRED`

- `validate_bank_checkout(transaction_id: str, otp: str)`: Validate a bank checkout

    - `transactionId`: Transaction id returned from a bank charge request. `REQUIRED`
    - `otp`: One Time Password provided by the customer you're charging. `REQUIRED`

- `bank_transfer(product_name: str, recipients: [dict])`: Move money form payment wallet to bank account.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `recipients`: A list of recipients. Each recipient has:

        - `bankAccount`: Bank account to receive money:

            - `accountName`: Name of the bank account. `REQUIRED`
            - `accountNumber`: Account number. `REQUIRED`
            - `bankCode`: A [6-Digit Integer Code](http://docs.africastalking.com/bank/checkout#bankCodes) for the bank that we allocate. See `payments::BANK*` for supported banks. `REQUIRED`
            - `dateOfBirth`: Date of birth of the account owner (in the format `YYYY-MM-DD`). Required for Zenith Bank Nigeria.

        - `currencyCode`: 3-digit ISO format currency code (only `NGN` is supported at present). `REQUIRED`
        - `amount`: Amount to pay. `REQUIRED`
        - `narration`: A short description of the transaction. `REQUIRED`
        - `metadata`: Additonal data to associate with the transaction. `REQUIRED`

- `card_checkout(product_name: str, currency_code:str, amount: float, payment_card: dict, narration: str, metadata: dict = {})`: Initiate card checkout.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `payment_card`: Payment card to be charged:

        - `number`: Payment card number. `REQUIRED`
        - `cvvNumber`: 3 or 4 digit card verification Value. `REQUIRED`
        - `expiryMonth`: Expiration month on the card (e.g `8`). `REQUIRED`
        - `authToken`: Payment card's ATM PIN. `REQUIRED`
        - `countryCode`: 2-Digit countryCode where the card was issued (only `NG` is supported at present). `REQUIRED`

    - `checkout_token`: A token that has been generated by our APIs as as result of charging a customers payment card in a previous transaction. When using a `checkoutToken`, the `paymentCard` data should NOT be populated.
    - `currency_code`: 3-digit ISO format currency code (only `NGN` is supported at present). `REQUIRED`
    - `amount`: Amount to charge. `REQUIRED`
    - `narration`: A short description of the transaction. `REQUIRED`
    - `metadata`: Additonal data to associate with the transaction. `REQUIRED`

- `validate_card_checkout(transaction_id: str, otp: str)`: Validate a card checkout

    - `transactionId`: Transaction id returned from a card charge request. `REQUIRED`
    - `otp`: One Time Password provided by the customer you're charging. `REQUIRED`

- `wallet_transfer(product_name: str, target_product_code: int, currency_code: str, amount: float, metadata: dict)`: Transfer money from one Payment Product to another Payment Product hosted on Africa's Talking.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `target_product_code`: Unique code ode of payment product receiving funds on Africa's Talking. `REQUIRED`
    - `currency_code`: 3-digit ISO format currency code (only `NGN` is supported at present). `REQUIRED`
    - `amount`: Amount to transfer. `REQUIRED`
    - `metadata`: Additional data to associate with the transation. `REQUIRED`


- `topup_stash(product_name: str, currency_code: str, amount: float, metadata: dict)`: Move money from a Payment Product to an app's stash.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `currency_code`: 3-digit ISO format currency code (only `NGN` is supported at present). `REQUIRED`
    - `amount`: Amount to transfer. `REQUIRED`
    - `metadata`: Additonal data to associate with the transaction. `REQUIRED`

- `fetch_product_transactions(product_name: str, filters: dict)`: Fetch transactions of a particular payment product.

    - `productName`: Payment product on Africa's Talking. `REQUIRED`
    - `pageNumber`: Page number to fetch results from. Starts from `1`. `REQUIRED`
    - `count`: Number of results to fetch. `REQUIRED`
    - `startDate`: Start Date to consider when fetching.
    - `endDate`: End Date to consider when fetching.
    - `category`: Category to consider when fetching.
    - `provider`: Provider to consider when fetching.
    - `status`: Status to consider when fetching.
    - `source`: Source to consider when fetching.
    - `destination`: Destination to consider when fetching.
    - `providerChannel`: Provider channel to consider when fetching.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
filters = {
    # pageNumber start from 1 and NOT 0
    "pageNumber": "1",
    "count": "100",
    # Date format has to be YYYY-MM-DD
    "startDate": "2018-01-01",
    "endDate": "2018-12-31",
    # Possible categories are: BankCheckout, CardCheckout, MobileCheckout, MobileC2B, MobileB2C, MobileB2B, BankTransfer, WalletTransfer, UserStashTopup
    "category": "UserStashTopup",
    # Providers include Mpesa, Segovia, Flutterwave, Admin, Athena
    "provider": "Athena",
    # Possible statuses are Success, Failed
    "status": "Failed",
    # Possible sources are phoneNumber, BankAccount, Card, Wallet
    "source": "phoneNumber",
    # Possible destinations are PhoneNumber, BankAccount, Card, Wallet
    "destination": "PhoneNumber",
    # Channel to consider e.g. Paybill Number
    "providerChannel": "1212"
}
res = payment.fetch_product_transactions(product_name='TestProduct', filters=filters)
```
- `find_transaction(transaction_id: str)`: Find a particular payment transaction.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.find_payment_transaction(transaction_id='ATPid_07c0c1776759d41beac6f77e43723489')
```
- `fetch_wallet_transactions(transaction_id: str)`: Fetch your wallet transactions.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
filters = {
    # pageNumber start from 1 and NOT 0
    "pageNumber": "1",
    "count": "100",
    # Date format has to be YYYY-MM-DD
    "startDate": "2018-01-01",
    "endDate": "2018-12-31",
    # Possible categories are: Debit, Credit, Refund, Topup
    "category": "Debit,Credit", # A comma delimited list of transaction categories you would like to consider.
}
res = payment.fetch_wallet_transactions(filters=filters)
```
- `fetch_wallet_balance()`: Fetch your wallet balance.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.fetch_wallet_balance()
```
    
    
    
    
    
## Services

All methods are synchronous (i.e. will block current thread) but provide asynchronous variants that take a callback `function (error: AfricasTalkingException, data: dict)`.

The synchronous variant always return and instance a `dict` while the async one returns a `Thread`.

All phone numbers use the international format. e.g. `+234xxxxxxxx`.

All **amount strings** contain currency code as well. e.g. `UGX 443.88`.


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
- `fetch_product_transactions(product_name: str, filters: dict)`: Fetch transactions of a particular payment product.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
filters = {
    # pageNumber start from 1 and NOT 0
    "pageNumber": "1",
    "count": "100",
    # Date format has to be YYYY-MM-DD
    "startDate": "2018-01-01",
    "endDate": "2018-12-31",
    # Possible categories are: BankCheckout, CardCheckout, MobileCheckout, MobileC2B, MobileB2C, MobileB2B, BankTransfer, WalletTransfer, UserStashTopup
    "category": "UserStashTopup",
    # Providers include Mpesa, Segovia, Flutterwave, Admin, Athena
    "provider": "Athena",
    # Possible statuses are Success, Failed
    "status": "Failed",
    # Possible sources are phoneNumber, BankAccount, Card, Wallet
    "source": "phoneNumber",
    # Possible destinations are PhoneNumber, BankAccount, Card, Wallet
    "destination": "PhoneNumber",
    # Channel to consider e.g. Paybill Number
    "providerChannel": "1212"
}
res = payment.fetch_product_transactions(product_name='TestProduct', filters=filters)
```
- `find_transaction(transaction_id: str)`: Find a particular payment transaction.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.find_payment_transaction(transaction_id='ATPid_07c0c1776759d41beac6f77e43723489')
```
- `fetch_wallet_transactions(transaction_id: str)`: Fetch your wallet transactions.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
filters = {
    # pageNumber start from 1 and NOT 0
    "pageNumber": "1",
    "count": "100",
    # Date format has to be YYYY-MM-DD
    "startDate": "2018-01-01",
    "endDate": "2018-12-31",
    # Possible categories are: Debit, Credit, Refund, Topup
    "category": "Debit,Credit", # A comma delimited list of transaction categories you would like to consider.
}
res = payment.fetch_wallet_transactions(filters=filters)
```
- `fetch_wallet_balance()`: Fetch your wallet balance.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.fetch_wallet_balance()
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
- `fetch_product_transactions(product_name: str, filters: dict)`: Fetch transactions of a particular payment product.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
filters = {
    # pageNumber start from 1 and NOT 0
    "pageNumber": "1",
    "count": "100",
    # Date format has to be YYYY-MM-DD
    "startDate": "2018-01-01",
    "endDate": "2018-12-31",
    # Possible categories are: BankCheckout, CardCheckout, MobileCheckout, MobileC2B, MobileB2C, MobileB2B, BankTransfer, WalletTransfer, UserStashTopup
    "category": "UserStashTopup",
    # Providers include Mpesa, Segovia, Flutterwave, Admin, Athena
    "provider": "Athena",
    # Possible statuses are Success, Failed
    "status": "Failed",
    # Possible sources are phoneNumber, BankAccount, Card, Wallet
    "source": "phoneNumber",
    # Possible destinations are PhoneNumber, BankAccount, Card, Wallet
    "destination": "PhoneNumber",
    # Channel to consider e.g. Paybill Number
    "providerChannel": "1212"
}
res = payment.fetch_product_transactions(product_name='TestProduct', filters=filters)
```
- `find_transaction(transaction_id: str)`: Find a particular payment transaction.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.find_payment_transaction(transaction_id='ATPid_07c0c1776759d41beac6f77e43723489')
```
- `fetch_wallet_transactions(transaction_id: str)`: Fetch your wallet transactions.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
filters = {
    # pageNumber start from 1 and NOT 0
    "pageNumber": "1",
    "count": "100",
    # Date format has to be YYYY-MM-DD
    "startDate": "2018-01-01",
    "endDate": "2018-12-31",
    # Possible categories are: Debit, Credit, Refund, Topup
    "category": "Debit,Credit", # A comma delimited list of transaction categories you would like to consider.
}
res = payment.fetch_wallet_transactions(filters=filters)
```
- `fetch_wallet_balance()`: Fetch your wallet balance.

```python
import africastalking
africastalking.initialize(username='sandbox', api_key='someKey')
payment = africastalking.Payment
res = payment.fetch_wallet_balance()
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
