from flask_wtf import FlaskForm
from wtforms import FileField, StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError, IPAddress #validatiemiddelen voor inputvelden
from cvf.models import User

## Account login input velden
class LoginFormulier(FlaskForm):
    username = StringField('Gebruikersnaam',
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember = BooleanField('Onthouden')
    submit = SubmitField('Login')

## Account registratie input velden
class RegistratieFormulier(FlaskForm):
    username = StringField('Gebruikersnaam',
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Wachtwoord', 
        validators=[DataRequired(), EqualTo('confirm_password', message='Wachtwoorden komen niet overeen')])
    confirm_password = PasswordField('Wachtwoord bevestigen',
        validators=[DataRequired(), EqualTo('password', message='Wachtwoorden komen niet overeen')])
    submit = SubmitField('Registreren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('Deze gebruikersnaam is al in gebruik')

## Account wijziging input velden
class WijzigingFormulier(FlaskForm):
    oldpassword = PasswordField('Wachtwoord', 
        validators=[DataRequired()])
    password = PasswordField('Nieuw wachtwoord', 
        validators=[DataRequired(), EqualTo('confirm_password', message='Wachtwoorden komen niet overeen')])
    confirm_password = PasswordField('Nieuw wachtwoord bevestigen',
        validators=[DataRequired(), EqualTo('password', message='Wachtwoorden komen niet overeen')])
    submit = SubmitField('Wijzigen')



