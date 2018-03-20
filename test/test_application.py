"""
Application

fetchApplicationData(): Fetch app info i.e. balance.
"""
import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Application


class TestApplicationService(unittest.TestCase):

    def test_fetch_account(self):
        res = service.fetch_application_data()
        assert res['UserData']['balance'] is not None


if __name__ == '__main__':
    unittest.main()
