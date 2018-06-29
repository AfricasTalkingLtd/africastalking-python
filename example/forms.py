from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SMSForm(FlaskForm):
  phone_number  = TelField("Phone Number", validators=[DataRequired()], render_kw={'placeholder': 'Phone Number eg. +254712345678'})
  sendSMS       = SubmitField("Send")

class AirtimeForm(FlaskForm):
  phone_number  = TelField("Phone Number", validators=[DataRequired()], render_kw={'placeholder': 'Phone Number eg. +254712345678'})
  amount        = StringField("Amount", validators=[DataRequired()], render_kw={'placeholder': 'Amount eg. KES 400'})
  sendAirtime   = SubmitField("Send Airtime")

class CheckOutForm(FlaskForm):
  phone_number  = TelField("Phone Number", validators=[DataRequired()], render_kw={'placeholder': 'Phone Number eg. +254712345678'})
  product_name  = StringField("Product Name", validators=[DataRequired()], render_kw={'placeholder': 'Braids'})
  currency_code = SelectField('Currency Code',choices = [('KES', 'KES'), ('USD', 'USD')])
  amount        = StringField("Amount", validators=[DataRequired()], render_kw={'placeholder': 'Amount eg. 400'})
  checkOut      = SubmitField("Send Money")

class B2CForm(FlaskForm):
	product_name = StringField("Product Name", validators=[DataRequired()], render_kw={'placeholder': 'Braids'})
	name         = StringField("name", validators=[DataRequired()], render_kw={'placeholder': 'Ann'})
	phone_number  = TelField("Phone Number", validators=[DataRequired()], render_kw={'placeholder': 'Phone Number eg. +254712345678'})
	currency_code= SelectField('Currency Code', choices  = [('KES', 'KES'), ('USD', 'USD')])
	amount        = StringField("Amount", validators=[DataRequired()], render_kw={'placeholder': 'Amount eg. 400'})
	send        = SubmitField("Send")


class VoiceForm(FlaskForm):
  source       = TelField("Source", validators=[DataRequired()], render_kw={'placeholder': 'Phone Number eg. +254712345678'})
  destination  = TelField("Destination", validators=[DataRequired()], render_kw={'placeholder': 'Phone Number eg. +254712345678'})
  call         = SubmitField("Call")

