import os
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

import africastalking

app = Flask(__name__)
api = Api(app)
CORS(app)

username = os.getenv('user_name', 'sandbox')
api_key = os.getenv('api_key', 'fake')

africastalking.initialize(username, api_key)
sms = africastalking.SMS
airtime  = africastalking.Airtime
checkout = africastalking.Payment
voice    = africastalking.Voice

class send_sms(Resource):
    def get(self):
      return {'hello': 'world'}
    def post(self):
      number = str(request.form['number'])
      return sms.send("Test message", [number])
api.add_resource(send_sms, '/sms')

class send_airtime(Resource):
    def get(self):
      return {'hello': 'world'}
    def post(self):
      number = str(request.form['number'])
      amount = str(request.form['amount'])
      return airtime.send(number, amount)
api.add_resource(send_airtime, '/airtime')

class mobile_checkout(Resource):
    def get(self):
      return {'hello': 'world'}
    def post(self):
      number = str(request.form['number'])
      product_name = str(request.form['product_name'])
      full_amount = str(request.form['amount'])
      currency_code = full_amount[0:3]
      amount = full_amount[4:]
      return checkout.mobile_checkout(product_name, number, currency_code, amount)
api.add_resource(mobile_checkout, '/mobile_checkout')

class mobile_b2c(Resource):
    def get(self):
      return {'hello': 'world'}
    def post(self):
      number = str(request.form['number'])
      product_name = str(request.form['product_name'])
      full_amount = str(request.form['amount'])
      currency_code = full_amount[0:3]
      amount = full_amount[4:]
      name = str(request.form['name'])
      recipients     = [
		{
			'name': name,
			'phoneNumber':number,
			'currencyCode':currency_code,
			'amount':amount,
			'metadata': {}
		}]
      return checkout.mobile_b2c(product_name, recipients)
api.add_resource(mobile_b2c, '/mobile_b2c')

if __name__ == '__main__':
    app.run(debug=True)
