# africastalking-python

![](https://img.shields.io/pypi/v/africastalking.svg)

> The SDK provides convenient access to the Africa's Talking APIs to python apps.


## Documentation
Take a look at the [API docs here](https://build.at-labs.io/discover/).

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

The package needs to be configured with your app username and API key, which you can get from the [dashboard](https://account.africastalking.com/).

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
- [Payments](#payments): `africastalking.Payment`
- [Voice](#voice): `africastalking.Voice`
- [Token](#token): `africastalking.Token`
- [Application](#application): `africastalking.Application`

### `Application`

- `fetch_application_data()`: Get app information. e.g balance.

### `Airtime`

- `send(recipients: [dict])`: Send airtime

    - `recipients`: Contains an array of arrays containing the following keys
    
        - `phone_number`: Recipient of airtime
        - `amount`: Amount to send with currency e.g `100`
        - `currency_code`: 3-digit ISO format currency code (e.g `KES`, `USD`, `UGX` etc).

### `Sms`

- `send(message: str, recipients: [str], sender_id: str = None, enqueue: bool = False)`: Send a message.

    - `message`: SMS content. `REQUIRED`
    - `recipients`: An array of phone numbers. `REQUIRED`
    - `sender_id`: Shortcode or alphanumeric ID that is registered with your Africa's Talking account.
    - `enqueue`: Set to `true` if you would like to deliver as many messages to the API without waiting for an acknowledgement from telcos.

- `send_premium(message: str, short_code: str, recipients: [str], link_id: [str] = None, retry_duration_in_hours [int] = None)`: Send a premium SMS

    - `message`: SMS content. `REQUIRED`
    - `short_code`: Your premium product shortCode. `REQUIRED`
    - `recipients`: An array of phone numbers. `REQUIRED`
    - `keyword`: Your premium product keyword.
    - `link_id`: We forward the `linkId` to your application when a user sends a message to your onDemand service
    - `retry_duration_in_hours`: This specifies the number of hours your subscription message should be retried in case it's not delivered to the subscriber

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
    
    
### `Payments`

- `mobile_checkout(product_name: str, phone_number: str, currency_code: str, amount: float, metadata: dict = {}, provider_channel:str)`: Charge a customers mobile money account

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `phone_number`: Customer phone number (in international format). `REQUIRED`
    - `currency_code`: 3-digit ISO format currency code (e.g `KES`, `USD`, `UGX` etc). `REQUIRED`
    - `amount`: Amount to charge. `REQUIRED`
    - `metadata`: Additional data to associate with the transaction. `REQUIRED`
    - `provider_channel`: The provider channel the payment will be initiated from e.g a paybill number. `OPTIONAL`
    
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
      - `requester`: PhoneNumber through which KPLC will send tokens when using B2B to buy electricity tokens.
      - `metadata`: Additional data to associate with the transaction. `REQUIRED`

- `mobile_data(product_name: str, recipients: dict)`: Send mobile data to customers.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `recipients`:  A list of recipients. Each recipient has:
      - `phoneNumber`: Customer phone number (in international format). `REQUIRED`
      - `quantity`: Mobile data amount. `REQUIRED`
      - `unit`: Mobile data unit. Can either be `MB` or `GB`. `REQUIRED`
      - `validity`: How long the mobile data is valid for. Must be one of `Day`, `Week` and `Month`. `REQUIRED`
      - `metadata`: Additional data to associate with the transaction. `REQUIRED`

- `bank_checkout(product_name: str, currency_code: str, amount: float, bank_account: dict, narration: str, metadata: dict = {})`: Initiate bank checkout.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `bank_account`: Bank account to be charged:

        - `accountName`: Name of the bank account. `REQUIRED`
        - `accountNumber`: Account number. `REQUIRED`
        - `bankCode`: A [6-Digit Integer Code](https://build.at-labs.io/docs/payments%2Fbank%2Fcheckout) for the bank that we allocate. See `payments::BANK*` for supported banks. `REQUIRED`
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
            - `bankCode`: A [6-Digit Integer Code](https://build.at-labs.io/docs/payments%2Fbank%2Fcheckout) for the bank that we allocate. See `payments::BANK*` for supported banks. `REQUIRED`
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
    - `filters`: Transaction filters.
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
    
- `wallet_transactions(filters: dict)`: Fetch your wallet transactions.

    - `filters`: Wallet transactions filters. `REQUIRED`
      - `pageNumber`: Page number to fetch results from. Starts from `1`. `REQUIRED`
      - `count`: Number of results to fetch. `REQUIRED`
      - `startDate`: Start Date to consider when fetching.
      - `endDate`: End Date to consider when fetching.
      - `category`: Comma delimited list of categories to consider when fetching.

- `find_transaction(transaction_id: str)`: Find a particular payment transaction.

    - `transaction_id`: ID of trancation to find. `REQUIRED`

- `wallet_balance()`: Fetch your wallet balance. 


### `Voice`

- `call(callFrom: str, callTo: [str])`: Initiate a phone call

	- `callFrom`: Phone number on Africa's Talking (in international format). `REQUIRED`
    - `callTo`: An array of phone numbers that you wish to dial (in international format). `REQUIRED`    

- `fetch_queued_calls(phone_number: str)`: Get queued calls

    - `phone_number`: Phone number mapped to your Africa's Talking account (in international format). `REQUIRED`

- `upload_media_file(phone_number: str, url: str)`: Upload voice media file

    - `phone_number`: phone number mapped to your Africa's Talking account (in international format). `REQUIRED`
    - `url`: The url of the file to upload. Should start with `http(s)://`. `REQUIRED`

### `Token`

- `create_checkout_token(phone_number: str)`: Create a new checkout token for `phone_number`.

    - `phone_number`: Phone number to create checkout token for

- `generate_auth_token()`: Generate an auth token to use for authentication instead of an API key.


### `Ussd`

For more information, please read [http://docs.africastalking.com/ussd](https://build.at-labs.io/docs/ussd%2Foverview)


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
