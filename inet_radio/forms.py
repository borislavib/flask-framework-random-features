from wtforms import Form
from wtforms import StringField, BooleanField, validators

class EditForm(Form):
    email = StringField('email')
    first_name = StringField('first_name', [validators.Length(min=0,max=5)])
    last_name = StringField('last_name', [validators.Length(max=255)])
    share_favourites = BooleanField('Share favourites', [validators.DataRequired()])


