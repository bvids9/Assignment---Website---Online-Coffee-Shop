from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# form used in basket
class CheckoutForm(FlaskForm):
    name = StringField("Your name", validators=[InputRequired()])
    email = StringField("Your email", validators=[InputRequired(), email()])
    phone = StringField("Your phone number", validators=[InputRequired()])
    address = StringField("Delivery Address", validators=[InputRequired()])
    submit = SubmitField("Send It!")

