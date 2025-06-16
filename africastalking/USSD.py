from .Service import APIService, validate_phone


class USSDService(APIService):
    def __init__(self, username, api_key):
        super(USSDService, self).__init__(username, api_key)

    def _init_service(self):
        super(USSDService, self)._init_service()
        self._baseUrl = self._baseUrl + "/version1/ussd"

    def build_menu(self, response_text, end_session=False):
        """
        Build a USSD menu response.
        
        Args:
            response_text (str): The text to display to the user
            end_session (bool): Whether to end the session (default: False)
            
        Returns:
            str: Properly formatted USSD response
        """
        if not isinstance(response_text, str):
            raise ValueError("response_text must be a string")
            
        prefix = "END" if end_session else "CON"
        return f"{prefix} {response_text}"

    def parse_ussd_input(self, text):
        """
        Parse USSD input text into menu levels.
        
        Args:
            text (str): The USSD input text (concatenated with '*')
            
        Returns:
            list: List of user inputs at each menu level
        """
        if not text:
            return []
        return text.split('*')

    def get_menu_level(self, text):
        """
        Get the current menu level based on user input.
        
        Args:
            text (str): The USSD input text
            
        Returns:
            int: Current menu level (0 for initial menu)
        """
        if not text:
            return 0
        return len(text.split('*'))

    def validate_ussd_request(self, session_id, phone_number, network_code, service_code, text):
        """
        Validate USSD request parameters.
        
        Args:
            session_id (str): Session ID
            phone_number (str): User's phone number
            network_code (str): Network code
            service_code (str): USSD service code
            text (str): User input text
            
        Returns:
            dict: Validation result with 'valid' boolean and 'errors' list
        """
        errors = []
        
        if not session_id:
            errors.append("session_id is required")
            
        if not phone_number:
            errors.append("phone_number is required")
        elif not validate_phone(phone_number):
            errors.append("Invalid phone number format")
            
        if not network_code:
            errors.append("network_code is required")
            
        if not service_code:
            errors.append("service_code is required")
            
        # text can be empty for initial request
        if text is None:
            errors.append("text parameter is required (can be empty string)")
            
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def checkout(self, product_name, phone_number, currency_code, amount, metadata=None, callback=None):
        """
        Initiate a checkout request for USSD payment.
        
        Args:
            product_name (str): Your payment product name
            phone_number (str): Customer's phone number
            currency_code (str): 3-letter ISO currency code
            amount (float): Amount to charge
            metadata (dict): Additional metadata (optional)
            callback (function): Callback function (optional)
            
        Returns:
            dict: API response
        """
        if not validate_phone(phone_number):
            raise ValueError("Invalid phone number: " + phone_number)
            
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
            
        if len(currency_code) != 3:
            raise ValueError("Currency code must be 3 characters")

        url = self._make_url("/checkout/request")
        data = {
            "username": self._username,
            "productName": product_name,
            "phoneNumber": phone_number,
            "currencyCode": currency_code,
            "amount": amount
        }
        
        if metadata:
            data["metadata"] = metadata

        return self._make_request(
            url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
        )

    def bank_checkout(self, product_name, bank_account, currency_code, amount, 
                     narration, metadata=None, callback=None):
        """
        Initiate a bank checkout request.
        
        Args:
            product_name (str): Your payment product name
            bank_account (dict): Bank account details
            currency_code (str): 3-letter ISO currency code
            amount (float): Amount to charge
            narration (str): Description of the transaction
            metadata (dict): Additional metadata (optional)
            callback (function): Callback function (optional)
            
        Returns:
            dict: API response
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
            
        if len(currency_code) != 3:
            raise ValueError("Currency code must be 3 characters")
            
        if not isinstance(bank_account, dict):
            raise ValueError("bank_account must be a dictionary")
            
        required_bank_fields = {'accountName', 'accountNumber', 'bankCode'}
        if not all(field in bank_account for field in required_bank_fields):
            raise ValueError("bank_account must contain: accountName, accountNumber, bankCode")

        url = self._make_url("/checkout/bank/request")
        data = {
            "username": self._username,
            "productName": product_name,
            "bankAccount": bank_account,
            "currencyCode": currency_code,
            "amount": amount,
            "narration": narration
        }
        
        if metadata:
            data["metadata"] = metadata

        return self._make_request(
            url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
        )

    def bank_transfer(self, product_name, recipients, callback=None):
        """
        Transfer money to bank accounts.
        
        Args:
            product_name (str): Your payment product name
            recipients (list): List of recipient dictionaries
            callback (function): Callback function (optional)
            
        Returns:
            dict: API response
        """
        if not isinstance(recipients, list) or len(recipients) == 0:
            raise ValueError("recipients must be a non-empty list")
            
        for recipient in recipients:
            if not isinstance(recipient, dict):
                raise ValueError("Each recipient must be a dictionary")
                
            required_fields = {'bankAccount', 'currencyCode', 'amount', 'narration'}
            if not all(field in recipient for field in required_fields):
                raise ValueError("Each recipient must contain: bankAccount, currencyCode, amount, narration")
                
            if not isinstance(recipient['amount'], (int, float)) or recipient['amount'] <= 0:
                raise ValueError("Amount must be a positive number")

        url = self._make_url("/transfer/bank")
        data = {
            "username": self._username,
            "productName": product_name,
            "recipients": recipients
        }

        return self._make_request(
            url,
            "POST",
            headers=self._headers,
            params=None,
            data=data,
            callback=callback,
        )
