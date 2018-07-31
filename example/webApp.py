import os
from flask import Flask, request, render_template
from flask_restful import Resource, Api

import africastalking

app = Flask(__name__)
api = Api(app)

username = os.getenv('user_name', 'sandbox')
api_key = os.getenv('api_key', 'fake')


africastalking.initialize(username, api_key)
sms = africastalking.SMS
airtime  = africastalking.Airtime
payment = africastalking.Payment
voice    = africastalking.Voice

@app.route('/')
def index():
    return render_template('index.html')

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
      return payment.mobile_checkout(product_name, number, currency_code, amount)
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
      return payment.mobile_b2c(product_name, recipients)
api.add_resource(mobile_b2c, '/mobile_b2c')

@app.route("/ussd", methods = ['GET', 'POST'])
def ussd():
  session_id   = request.values.get("sessionId", None)
  serviceCode  = request.values.get("serviceCode", None)
  phone_number = request.values.get("phoneNumber", None)
  text         = request.values.get("text", "default")

  if text      == '':
      response  = "CON What would you want to check \n"
      response += "1. My Account \n"
      response += "2. My phone number"

  elif text    == '1':
      response  = "CON Choose account information you want to view \n"
      response += "1. Account number \n"
      response += "2. Account balance"

  elif text   == '2':
      response = "END Your phone number is " + phone_number

  elif text          == '1*1':
      accountNumber  = "ACC1001"
      response       = "END Your account number is " + accountNumber

  elif text    == '1*2':
      balance  = "KES 10,000"
      response = "END Your balance is " + balance

  else :
      response = "END Invalid choice"

  return response

if __name__ == '__main__':
    app.run(debug=True)

