import africastalking, json

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import SMSForm, AirtimeForm, CheckOutForm, VoiceForm, B2CForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd67cf7963921cd7f01f8ea3d3cef0857'

# Initialize SDK
username = "sandbox"    # use 'sandbox' for development in the test environment
api_key = "61e711157d969e942234f562c6d70ad62ef6d903de85de6f8e152ed381637373"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)
sms = africastalking.SMS
airtime = africastalking.Airtime
checkout = africastalking.Payment
voice = africastalking.Voice

@app.route("/")
@app.route("/home",methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route("/sendSMS", methods=['GET', 'POST'])
def sendSMS():
	form = SMSForm()
	if request.method == "POST":
		number = request.values['phone_number']
		json.dumps(sms.send("How are you doing today", [number]))
		return redirect(url_for('home'))
	return render_template('form.html', form=form)

@app.route("/sendAirtime", methods=['GET', 'POST'])
def sendAirtime():
	form = AirtimeForm(data=request.form)
	if request.method == "POST":
		number = request.values['phone_number']
		amount = request.values['amount']
		json.dumps(airtime.send(number, amount))
		return redirect(url_for('home'))
	return render_template('form.html', form=form)

@app.route("/mobilecheckout", methods=['GET', 'POST'])
def mobilecheckout():
	form = CheckOutForm(data=request.form)
	if request.method == "POST":
		number = request.values['phone_number']
		product_name = request.values['product_name']
		currency_code = request.values['currency_code']
		amount = request.values['amount']
		json.dumps(checkout.mobile_checkout(product_name, number, currency_code, amount))
		return redirect(url_for('home'))
	return render_template('form.html', form=form)

@app.route("/mobileB2C", methods=['GET', 'POST'])
def mobileB2C():
	form = B2CForm(data=request.form)
	if request.method == "POST":
		product_name = request.values['product_name']
		recipients = [
		{
			'name': request.values['name'],
			'phoneNumber':request.values['phone_number'],
			'currencyCode':request.values['currency_code'],
			'amount':request.values['amount'],
			'metadata': {}
		}]
		json.dumps(checkout.mobile_b2c(product_name, recipients))
		return redirect(url_for('home'))
		
	return render_template('form.html', form=form)

@app.route("/VoiceCall", methods=['GET', 'POST'])
def VoiceCall():
	form = VoiceForm()
	if request.method == "POST":
		source = request.values['source']
		destination = request.values['destination']
		#voice.call(source, destination)
		json.dumps(voice.call(source, destination))
		return redirect(url_for('home'))
	return render_template('form.html', form=form)

@app.route("/USSD", methods=['GET', 'POST'])
def USSD():
	session_id = request.values.get("sessionId", None)
	serviceCode = request.values.get("serviceCode", None)
	phone_number = request.values.get("phoneNumber", None)
	text = request.values.get("text", "default")

	if text == '':
	    response  = "CON What would you want to check \n"
	    response += "1. My Account \n"
	    response += "2. My phone number"

	elif text == '1':
	    response = "CON Choose account information you want to view \n"
	    response += "1. Account number \n"
	    response += "2. Account balance"

	elif text == '2':
	    response = "END Your phone number is " + phone_number

	elif text == '1*1':
	    accountNumber  = "ACC1001"
	    response = "END Your account number is " + accountNumber

	elif text == '1*2':
	    balance  = "KES 10,000"
	    response = "END Your balance is " + balance

	else :
	    response = "END Invalid choice"

	return response

	#return render_template('home.html')
if __name__ == '__main__':
    app.run(debug = True)

