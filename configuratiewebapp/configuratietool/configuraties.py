from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import Optional, DataRequired, InputRequired, Length, Email, EqualTo, ValidationError, IPAddress # validatiemiddelen voor inputvelden


## Configuratie generatie input velden
class ConfiguratieFormulier(FlaskForm):
   configuratie_vpn = TextAreaField('VPN')
    
   configuratie_interface_wan_ip = StringField("WAN IP",
   validators=[Optional(), IPAddress(message="Geen valide IP!")])

   configuratie_fanServer = StringField("Fortianalyzer Server")
   configuratie_fanSerial = StringField("Fortianalyzer Serial")
   
   
   submit = SubmitField('Genereren')

