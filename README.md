# africastalking-python

> The wrapper provides convenient access to the Africa's Talking API from applications written in Python.


## Documentation
Take a look at the [API docs here](http://docs.africastalking.com).

## Install

```bash
$ pip  install africastalking # python 2.x
```


## Usage

```python
# import package
import africastalking


# Initialize SDK
username = "YOUR_USERNAME"    # use 'sandbox' for development in the test environment
api_key = "YOUR_API_KEY"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.get_sms_service()


# Use the service
response = sms.send("Hello Message!", ["2547xxxxxx"])
```

See [example](example/) for more usage examples.


## Initialization

The following static methods are available in the `africastalking` module to initialize the library:

- `initialize(username, api_key)`: Initialize the library.

- `get_xxx_service()`: Get an instance to a given service by name or by class.

## Services

All methods return a `dict`. All methods are synchronous (i.e. will block current thread) but provide asynchronous variants that take a `Callback(error: AfricasTalkingException, data: dict)` as the last argument.

### `AccountService`

- `fetch_account()`: Get app balance info.

### `AirtimeService`

- `send(phone_number, amount)`: Send airtime to a phone number. Example amount would be `KES 150`.

- `send(recipients)`: Send airtime to a bunch of phone numbers. The keys in the `recipients` map are phone numbers while the values are airtime amounts. The amounts need to have currency info e.g. `UXG 4265`.

For more information about status notification, please read [http://docs.africastalking.com/airtime/callback](http://docs.africastalking.com/airtime/callback)


### `SmsService`

- `send(message, recipients, sender_id = None, enqueue = False)`: Send a bulk message to recipients, optionally from sender_id (Short Code or Alphanumeric).

- `send_premium(message, keyword, link_id, recipients)`: Send a premium SMS

- `fetch_messages(last_received_id = 0)`: Fetch your messages

- `fetch_subscriptions(short_code, keyword, last_received_id = 0)`: Fetch your premium subscription data

- `create_subscription(short_code, keyword, phone_number, checkout_token)`: Create a premium subscription

For more information on: 

- How to receive SMS: [http://docs.africastalking.com/sms/callback](http://docs.africastalking.com/sms/callback)
- How to get notified of delivery reports: [http://docs.africastalking.com/sms/deliveryreports](http://docs.africastalking.com/sms/deliveryreports)
- How to listen for subscription notifications: [http://docs.africastalking.com/subscriptions/callback](http://docs.africastalking.com/subscriptions/callback)

### `TokenService`

- `create_checkout_token(phone_number)`: Create a new checkout token for `phone_number`.

- `generate_auth_token()`: Generate an auth token to use for authentication instead of an API key.



## Development
```shell
$ git clone https://github.com/aksalj/africastalking-python.git
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