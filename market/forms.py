from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import user


class register_form(FlaskForm):

    def validate_username(self, check_username):
        username = user.query.filter_by(username=check_username.data).first()
        if username:
            raise ValidationError("Username already exists!")

    def validate_email(self, check_email):
        email = user.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError("Email already exists!")

    username = StringField(label="User Name", validators=[Length(min=3, max=30), DataRequired()])
    email = StringField(label="Email Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=5), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")

class login_form(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="LogIn")

class purchase_item(FlaskForm):
    submit = SubmitField(label="Purchase Item!")

class sell_item(FlaskForm):
    submit = SubmitField(label="Sell Item!")