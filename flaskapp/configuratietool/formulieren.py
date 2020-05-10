from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError #validatiemiddelen voor inputvelden
from configuratietool.models import User

## Login input velden
class LoginFormulier(FlaskForm):
    username = StringField('Gebruikersnaam',
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember = BooleanField('Onthouden')
    submit = SubmitField('Login')

## Registratie input velden
class RegistratieFormulier(FlaskForm):
    username = StringField('Gebruikersnaam',
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Wachtwoord', 
        validators=[DataRequired()])
    confirm_password = PasswordField('Wachtwoord bevestigen',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registreren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Gebruikersnaam al in gebruik')