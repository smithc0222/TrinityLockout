from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SelectField, validators

class LockoutForm(Form):
    lockout_number=StringField('LOTO Number:', [validators.Length(min=3)])
    lockout_description=StringField('Description', [validators.Length(min=2, max=300)])
    goggles=BooleanField('Goggles')
    faceshield=BooleanField('Face Shield')
    fullface=BooleanField('Full Face Respirator')
    dustmask=BooleanField('Dust Mask')
    leathergloves=BooleanField('Leather Gloves')
    saranax=BooleanField('Saranax Suit')
    nitrilegloves=BooleanField('Nitrile Gloves')
    chemicalgloves=BooleanField('Chemical Gloves')
    chemicalsuit=BooleanField('Chemical Suit')
    tyrex=BooleanField('Tyrex Suit')
    rubberboots=BooleanField('Rubber Boots')
    sar=BooleanField('SAR')
    ppe=StringField('Other PPE:', [validators.Length(max=50)])

class LockoutLineForm(Form):
    valve_number=StringField(u'',[validators.Length(max=10)])
    line_description=StringField(u'',[validators.Length(max=50)])
    lock_position=SelectField(u'', choices=[('open','Open'),('close','Close')])
    removal_position=SelectField(u'', choices=[('open','Open'),('close','Close')])

class ImplementedForm(Form):
    implemented_by=StringField('Implemented by:')
    
class AcceptedForm(Form):
    accepted_by=StringField('Accepted by:')

class ReleasedForm(Form):
    released_by=StringField('Released by:')

class ClearedForm(Form):
    cleared_by=StringField('Cleared by:')

def validate_lockout_number(self, field):
    if Lockout.query.filter_by(lockout_number=field.data).first():
        raise ValidationError('Lockout number already in use.')
