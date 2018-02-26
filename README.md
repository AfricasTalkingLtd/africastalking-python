# africastalking-python

> The wrapper provides convenient access to the Africa's Talking API from applications written in Python.


## Documentation
Take a look at the [API docs here](http://docs.africastalking.com).

## Install

```bash
$ pip  install africastalking # python 2.x

OR

$ pip3 install africastalking # on python 3.x
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
sms = africastalking.get_service(africastalking.SERVICE.SMS)


# Use the service
response = sms.send("Hello Message!", ["2547xxxxxx"])
```

See [example](example/) for more usage examples.


## Initialization

The following static methods are available in the `africastalking` module to initialize the library:

- `initialize(username, api_key)`: Initialize the library.

- `get_service(africastalking.SERVICE.*)`: Get an instance to a given service by name or by class.

## Services






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