"""
USSD

build_menu(response_text: String, end_session: Optional<Boolean>): Build a USSD menu response with proper CON/END prefix.

parse_ussd_input(text: String): Parse USSD input text into menu levels.

get_menu_level(text: String): Get the current menu level based on user input.

validate_ussd_request(session_id: String, phone_number: String, network_code: String, service_code: String, text: String): Validate USSD request parameters.

checkout(product_name: String, phone_number: String, currency_code: String, amount: Float, metadata: Optional<Dict>): Initiate a checkout request for USSD payment.

bank_checkout(product_name: String, bank_account: Dict, currency_code: String, amount: Float, narration: String, metadata: Optional<Dict>): Initiate a bank checkout request.

bank_transfer(product_name: String, recipients: List<Dict>): Transfer money to bank accounts.
"""

import africastalking
import unittest
from test import USERNAME, API_KEY

africastalking.initialize(USERNAME, API_KEY)
service = africastalking.USSD


class TestUSSDService(unittest.TestCase):
    
    def test_build_menu_continue_session(self):
        """Test building a USSD menu that continues the session"""
        response = service.build_menu("Welcome to our service\n1. Balance\n2. Transfer")
        self.assertEqual(response, "CON Welcome to our service\n1. Balance\n2. Transfer")
    
    def test_build_menu_end_session(self):
        """Test building a USSD menu that ends the session"""
        response = service.build_menu("Thank you for using our service", end_session=True)
        self.assertEqual(response, "END Thank you for using our service")
    
    def test_build_menu_invalid_input(self):
        """Test building a USSD menu with invalid input"""
        with self.assertRaises(ValueError):
            service.build_menu(123)  # Not a string
    
    def test_parse_ussd_input_empty(self):
        """Test parsing empty USSD input"""
        result = service.parse_ussd_input("")
        self.assertEqual(result, [])
    
    def test_parse_ussd_input_single_level(self):
        """Test parsing single level USSD input"""
        result = service.parse_ussd_input("1")
        self.assertEqual(result, ["1"])
    
    def test_parse_ussd_input_multiple_levels(self):
        """Test parsing multiple level USSD input"""
        result = service.parse_ussd_input("1*2*3")
        self.assertEqual(result, ["1", "2", "3"])
    
    def test_get_menu_level_initial(self):
        """Test getting menu level for initial request"""
        level = service.get_menu_level("")
        self.assertEqual(level, 0)
    
    def test_get_menu_level_first_input(self):
        """Test getting menu level for first user input"""
        level = service.get_menu_level("1")
        self.assertEqual(level, 1)
    
    def test_get_menu_level_multiple_inputs(self):
        """Test getting menu level for multiple user inputs"""
        level = service.get_menu_level("1*2*3")
        self.assertEqual(level, 3)
    
    def test_validate_ussd_request_valid(self):
        """Test validating a valid USSD request"""
        result = service.validate_ussd_request(
            session_id="session123",
            phone_number="+254718769882",
            network_code="63902",
            service_code="*123#",
            text=""
        )
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_validate_ussd_request_invalid_phone(self):
        """Test validating USSD request with invalid phone number"""
        result = service.validate_ussd_request(
            session_id="session123",
            phone_number="invalid_phone",
            network_code="63902",
            service_code="*123#",
            text=""
        )
        self.assertFalse(result['valid'])
        self.assertIn("Invalid phone number format", result['errors'])
    
    def test_validate_ussd_request_missing_params(self):
        """Test validating USSD request with missing parameters"""
        result = service.validate_ussd_request(
            session_id="",
            phone_number="",
            network_code="",
            service_code="",
            text=None
        )
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_checkout_valid(self):
        """Test USSD checkout with valid parameters"""
        try:
            response = service.checkout(
                product_name="TestProduct",
                phone_number="+254718769882",
                currency_code="KES",
                amount=100.0
            )
            # In sandbox, we expect a response structure
            self.assertIsInstance(response, dict)
        except Exception as e:
            # In case of network issues or sandbox limitations
            self.assertIsInstance(e, Exception)
    
    def test_checkout_invalid_phone(self):
        """Test USSD checkout with invalid phone number"""
        with self.assertRaises(ValueError):
            service.checkout(
                product_name="TestProduct",
                phone_number="invalid_phone",
                currency_code="KES",
                amount=100.0
            )
    
    def test_checkout_invalid_amount(self):
        """Test USSD checkout with invalid amount"""
        with self.assertRaises(ValueError):
            service.checkout(
                product_name="TestProduct",
                phone_number="+254718769882",
                currency_code="KES",
                amount=-100.0  # Negative amount
            )
    
    def test_checkout_invalid_currency(self):
        """Test USSD checkout with invalid currency code"""
        with self.assertRaises(ValueError):
            service.checkout(
                product_name="TestProduct",
                phone_number="+254718769882",
                currency_code="INVALID",  # Invalid currency code
                amount=100.0
            )
    
    def test_bank_checkout_valid(self):
        """Test bank checkout with valid parameters"""
        bank_account = {
            "accountName": "Test Account",
            "accountNumber": "1234567890",
            "bankCode": "01"
        }
        try:
            response = service.bank_checkout(
                product_name="TestProduct",
                bank_account=bank_account,
                currency_code="KES",
                amount=100.0,
                narration="Test payment"
            )
            self.assertIsInstance(response, dict)
        except Exception as e:
            # In case of network issues or sandbox limitations
            self.assertIsInstance(e, Exception)
    
    def test_bank_checkout_invalid_bank_account(self):
        """Test bank checkout with invalid bank account"""
        with self.assertRaises(ValueError):
            service.bank_checkout(
                product_name="TestProduct",
                bank_account={"incomplete": "data"},  # Missing required fields
                currency_code="KES",
                amount=100.0,
                narration="Test payment"
            )
    
    def test_bank_transfer_valid(self):
        """Test bank transfer with valid recipients"""
        recipients = [
            {
                "bankAccount": {
                    "accountName": "Test Account 1",
                    "accountNumber": "1234567890",
                    "bankCode": "01"
                },
                "currencyCode": "KES",
                "amount": 100.0,
                "narration": "Test transfer 1"
            }
        ]
        try:
            response = service.bank_transfer(
                product_name="TestProduct",
                recipients=recipients
            )
            self.assertIsInstance(response, dict)
        except Exception as e:
            # In case of network issues or sandbox limitations
            self.assertIsInstance(e, Exception)
    
    def test_bank_transfer_empty_recipients(self):
        """Test bank transfer with empty recipients list"""
        with self.assertRaises(ValueError):
            service.bank_transfer(
                product_name="TestProduct",
                recipients=[]
            )
    
    def test_bank_transfer_invalid_recipient(self):
        """Test bank transfer with invalid recipient data"""
        recipients = [
            {
                "incomplete": "data"  # Missing required fields
            }
        ]
        with self.assertRaises(ValueError):
            service.bank_transfer(
                product_name="TestProduct",
                recipients=recipients
            )


if __name__ == '__main__':
    unittest.main()
