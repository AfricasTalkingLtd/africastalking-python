#!/usr/bin/env python
import os
from dotenv import load_dotenv
import africastalking

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)


def main():
    africastalking.initialize(username=os.environ.get('USERNAME'), api_key=os.environ.get('API_KEY'))
    sms = africastalking.SMS

    def on_finish(error, data):
        if error is not None:
            raise error

        print '\nAsync Done with -> ' + str(data['SMSMessageData']['Message'])

    # Send SMS asynchronously
    sms.send('Hello Async', ['+254718769882'], callback=on_finish)
    print 'Waiting for async result....'
    # Send SMS synchronously
    result = sms.send('Hello Sync Test', ['+254718769882'])
    print '\nSync Done with -> ' + result['SMSMessageData']['Message']


if __name__ == "__main__":
    main()
