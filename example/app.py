#!/usr/bin/env python
import os
from dotenv import load_dotenv
import africastalking

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)


def main():
    africastalking.initialize(username=os.environ.get('USERNAME'), api_key=os.environ.get('API_KEY'))
    token = africastalking.get_service(africastalking.SERVICE_TOKEN)
    account = africastalking.get_service(africastalking.SERVICE_ACCOUNT)
    airtime = africastalking.get_service(africastalking.SERVICE_AIRTIME)

    def cb(error, data):
        if error is not None:
            raise error

        print data

    token.create_checkout_token('0718768998', callback=cb)
    account.fetch_account(cb)
    airtime.send(recipients = [{
        'phoneNumber': '+254718769882',
        'amount': 'KES 67.33'
    }], callback=cb)
    print 'Waiting for result....'
    # res = token.generate_auth_token()
    # print res


if __name__ == "__main__":
    main()
