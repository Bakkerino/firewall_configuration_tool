from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import Optional, DataRequired, InputRequired, Length, Email, EqualTo, ValidationError, IPAddress # validatiemiddelen voor inputvelden

## legacy ##

## Configuratie generatie input velden
class ConfigurationForm(FlaskForm):
   configuratie_vpn = TextAreaField('VPN')
    
   configuratie_interface_wan_ip = StringField("WAN IP",
   validators=[Optional(), IPAddress(message="Geen valide IP!")])

   configuratie_fanServer = StringField("Fortianalyzer Server")
   configuratie_fanSerial = StringField("Fortianalyzer Serial")
   
   
   submit = SubmitField('Genereren')

def genFortianalyzer(server, serial):
    outputData = []
    outputData.append((f"""config log fortianalyzer setting
 set status enable
 set server \""""  + server +  """\" 
 set serial """ + serial + """
end\n"""))
    outputData.append("Fortianalyzer is aangezet, met server: " + server + " en serial: " + serial)
    return outputData

