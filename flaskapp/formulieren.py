from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo #validatiemiddelen voor inputvelden

## Login input velden
class LoginFormulier(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember = BooleanField('Onthouden')
    submit = SubmitField('Login')

## Registratie input velden
class RegistratieFormulier(FlaskForm):
    username = StringField('Gebruikersnaam',
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', 
        validators=[DataRequired()])
    confirm_password = PasswordField('Wachtwoord bevestigen',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registreren')

