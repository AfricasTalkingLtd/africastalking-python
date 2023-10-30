import sys

sys.path.append(
    "/Users/nicholasngatia/Documents/yoda/africastalking-python/africastalking"
)
import africastalking

africastalking.initialize("test", "api_key")
service = africastalking.MobileData
res = service.send(
    product_name="Mobile Data",
    recipients=[
        {
            "phoneNumber": "+254705212848",
            "quantity": 1,
            "unit": "GB",
            "validity": "Week",
            "isPromoBundle": False,
            "metadata": {
                "isTesting": "false",
                "first_name": "Daggie",
                "last_name": "Blanqx",
            },
        }
    ],
)
print(res)
