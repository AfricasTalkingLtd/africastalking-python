# africastalking-python

![](https://img.shields.io/pypi/v/africastalking.svg)

> The SDK provides convenient access to the Africa's Talking APIs to python apps.


## Documentation
Take a look at the [API docs here](https://developers.africastalking.com).

## Install

```bash
$ pip3 install africastalking # python 3.8.x

OR

$ python3 -m pip install africastalking # python 3.8.x

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
- [Voice](#voice): `africastalking.Voice`
- [Token](#token): `africastalking.Token`
- [Application](#application): `africastalking.Application`
- [Mobile Data](#mobiledata): `africastalking.MobileData`
- [Insights](#insights): `africastalking.Insights`
- [Whatsapp](#whatsapp): `africastalking.Whatsapp`

### `Application`

- `fetch_application_data()`: Get app information. e.g balance.

### `Airtime`

- `send(recipients: [dict])`: Send airtime

    - `recipients`: Contains an array of arrays containing the following keys
    
        - `phone_number`: Recipient of airtime
        - `amount`: Amount to send with currency e.g `100`
        - `currency_code`: 3-digit ISO format currency code (e.g `KES`, `USD`, `UGX` etc).

- `max_num_retry`: This allows you to specify the maximum number of retries in case of failed airtime deliveries due to various reasons such as telco unavailability. The default retry period is 8 hours and retries occur every 60 seconds. For example, setting `max_num_retry=4` means the transaction will be retried every 60 seconds for the next 4 hours. `OPTIONAL`.

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

- `create_safaricom_subscription(short_code: str, keyword: str, phone_number: str, request_id: str, redirect_url: str, source_ip: str, user_agent: str)`: Create a premium Safaricom subscription

    - `short_code`: Premium short code mapped to your account. `REQUIRED`
    - `keyword`: Premium keyword under the above short code and is also mapped to your account. `REQUIRED`
    - `request_id`: Request id associated with the request.
    - `redirect_url`: URL that the user will be redirected to after they have confirmed their subscription. 
    - `phone_number`: PhoneNumber to be subscribed.
    - `source_ip`: IP address the subscribing party is originating from.
    - `user_agent`: String stating which browser was used to access the content.

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

- `generate_auth_token()`: Generate an auth token to use for authentication instead of an API key.

### `MobileData`

- `send(product_name: str, recipients: dict)`: Send mobile data to customers.

    - `product_name`: Payment product on Africa's Talking. `REQUIRED`
    - `recipients`:  A list of recipients. Each recipient has:
      - `phoneNumber`: Customer phone number (in international format). `REQUIRED`
      - `quantity`: Mobile data amount. `REQUIRED`
      - `unit`: Mobile data unit. Can either be `MB` or `GB`. `REQUIRED`
      - `validity`: How long the mobile data is valid for. Must be one of `Day`, `Week` and `Month`. `REQUIRED`
      - `metadata`: Additional data to associate with the transaction. `OPTIONAL`

- `find_transaction(transaction_id: str)`: Find a mobile data transaction.

- `fetch_wallet_balance()`: Fetch a mobile data product balance.

### `Insights`

- `check_sim_swap_state(phone_numbers: [str])`: Check the sim swap state of a given [array of ] phone number(s).

### `Whatsapp`

- `send(body: dict, wa_number: str, phone_number: str)`: Send a whatsapp message to a given phone number.

    - `wa_number`: The number being used to send the message that is associated with the account. `REQUIRED`
    - `phone_number`: The number that is to receive the message. `REQUIRED`
    - `body`:  The message to be sent. The message has a combination of the following:
      - `message`: The message to be sent to the client. `OPTIONAL`
      - `mediaType`: The type of message being sent Can be one of `Image`, `Video`, `Audio` or `Voice`. `OPTIONAL`
      - `url`: The hosted URL of what is being sent. `OPTIONAL`
      - `caption`: The caption associated with an image or video that is being sent. `OPTIONAL`
      - `action`: A dictionary with a list of actions. `OPTIONAL`
      - `body`: A dictionary containing what is being sent with the interactive button or list. `OPTIONAL`
      - `header`: A dictionary containing what header is being sent with the interactive button or list.`OPTIONAL`
      - `footer`: A dictionary containing what footer is being sent with the interactive button or list.`OPTIONAL`

- `send_template(component: dict, wa_number: str, name: str, language: str, category: str)`: Send a Whatsapp template for your future messages.

    - `wa_number`: The Whatsapp phone number that will be used to send the messages associated with the template. `REQUIRED`
    - `name`: The name of the template. This must be unique. `REQUIRED`
    - `language`: The language code associated with the template. `REQUIRED`
    - `category`: The category associated with the template. `REQUIRED`
    - `component`:  A complex type containing the values that will be in the template. It can contain the following types:
      - `header`: The header of the template to be sent. `OPTIONAL`
      - `body`: The type of message being sent in the body of the template. `OPTIONAL`
      - `footer`: The footer of the template to be sent. `OPTIONAL`
      - `buttons`: A list of buttons to be sent in the template. `OPTIONAL`

### `Ussd`

For more information, please read [https://developers.africastalking.com/docs/ussd](https://developers.africastalking.com/docs/ussd/overview)


## Development
```shell
$ git clone https://github.com/AfricasTalkingLtd/africastalking-python.git
$ cd africastalking-python
$ python3 -m unittest
```

## Issues

If you find a bug, please file an issue on [our issue tracker on GitHub](https://github.com/AfricasTalkingLtd/africastalking-python/issues).
