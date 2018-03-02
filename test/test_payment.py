"""
Payment

cardCheckout(productName: String, amount: String, paymentCard: PaymentCard): Initiate card checkout.

validateCardCheckout(transactionId: String, token: String): Validate a card checkout

bankCheckout(productName: String, amount: String, bankAccount: BankAccount): Initiate bank checkout.

validateBankCheckout(transactionId: String, token: String): Validate a bank checkout

bankTransfer(productName: String, recipients: List<Bank>): Move money form payment wallet to bank account

mobileCheckout(productName: String, phoneNumber: String, amount: String): Initiate mobile checkout.

mobileB2C(productName: String, consumers: List<Consumer>): Send mobile money to consumers.

mobileB2B(productName: String, recipient: Business): Send mobile money to a business.
"""
import africastalking
import unittest
import random
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.Payment


class TestPaymentService(unittest.TestCase):

    def test_mobile_checkout(self):
        res = service.mobile_checkout(product_name='TestProduct', phone_number='+254718769882', amount="USD 10")
        assert res['status'] == 'PendingConfirmation'

    def test_mobile_b2c(self):
        consumer = {
            'name': 'Salama',
            'phoneNumber': '+254718769882',
            'currencyCode': 'KES',
            'amount': 892,
            # Optionals
            'reason': service.REASON['SalaryPayment'],
            'providerChannel': '1212',
            'metadata': {}
        }
        res = service.mobile_b2c(product_name='TestProduct', consumers=[consumer])
        assert res['totalValue'] == 'KES 892.0000'

    def test_mobile_b2b(self):
        business = {
            'provider': 'Athena',
            'transferType': 'BusinessToBusinessTransfer',
            'currencyCode': 'KES',
            'amount': 892.78,
            'destinationChannel': 'ABC',
            'destinationAccount': 'DEF',
            # Optionals
            'metadata': {}
        }
        res = service.mobile_b2b(product_name='TestProduct', business=business)
        assert res['status'] == 'Queued'

    def test_bank_transfer(self):
        recipient = {
            'bankAccount': {
                'accountNumber': '2342342343',
                'bankCode': service.BANK['FCMB_NG'],
                # Optionals
                'accountName': 'Salama',
            },
            'currencyCode': 'NGN',
            'amount': 89233.89 + random.randint(32, 7783),
            'narration': 'Test transfer',
            # Optionals
            'metadata': {}
        }
        res = service.bank_transfer(product_name='TestProduct', recipients=[recipient])
        assert res['entries'][0]['status'] == 'Queued'

    def test_bank_checkout(self):
        bank_account = {
            'accountNumber': '2342342343',
            'bankCode': service.BANK['FCMB_NG'],
            # Optionals
            'accountName': 'Salama',
            'dateOfBirth': '2001-11-21',
        }
        amount = 'NGN ' + str(783 + random.randint(34, 77742))
        res = service.bank_checkout(product_name='TestProduct', amount=amount,
                                    bank_account=bank_account, narration='Hello')
        assert res['status'] == 'PendingValidation'

    def test_validate_bank_checkout(self):
        fake_id = '624241f8' + str(random.randint(34, 43332))
        res = service.validate_bank_checkout(transaction_id=fake_id, otp=4433)
        assert res['status'] == 'InvalidRequest'

    def test_validate_card_checkout(self):
        fake_id = '624241f8' + str(random.randint(34, 43332))
        res = service.validate_card_checkout(transaction_id=fake_id, otp=4433)
        assert res['status'] == 'InvalidRequest'

    def test_card_checkout(self):
        card = {
            'number': '9223372036854775807',
            'cvvNumber': 2233,
            'expiryMonth': 11,
            'expiryYear': 2049,
            'countryCode': 'NG',
            'authToken': '3323'
        }
        amount = 'NGN ' + str(783 + random.randint(34, 77742))
        res = service.card_checkout(product_name='TestProduct', amount=amount,
                                    payment_card=card, narration='Hello')
        assert res['status'] == 'PendingValidation'


if __name__ == '__main__':
    unittest.main()
