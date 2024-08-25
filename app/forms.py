from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, DateTimeField, PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app import db
import sqlalchemy as sa
from .models import User
from string import punctuation


class ShopForm(FlaskForm):
    title = StringField('Product name', validators=[DataRequired()])
    description = TextAreaField('Proudct description', validators=[DataRequired()])
    photo = FileField('photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    seller = StringField('Seller name', validators=[DataRequired()])
    price = FloatField('Product price', validators=[DataRequired()])
    # time = DateTimeField('Time', format='%Y.%m.%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing up')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email already exists')

    def validate_password(self, password):
        validation_dct = {
            'digit': 0,
            'upper': 0,
            'lower': 0,
            'symbol': 0
        }
        for i in password.data:
            if i.isdigit():
                validation_dct['digit'] += 1
            if i.isupper():
                validation_dct['upper'] += 1
            if i.islower():
                validation_dct['lower'] += 1
            if i in punctuation:
                validation_dct['symbol'] += 1

        errors = []
        if len(password.data) < 8:
            errors.append('Password length must be grater or equal than 8')
        if not validation_dct['digit']:
            errors.append('Password must contain at least one number')
        if not validation_dct['upper']:
            errors.append('Password must contain at least one upper letter')
        if not validation_dct['lower']:
            errors.append('Password must contain at least one lower letter')
        if not validation_dct['symbol']:
            errors.append('Password must contain at least one symbol')
        if errors:
            raise ValidationError(', '.join(errors))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')