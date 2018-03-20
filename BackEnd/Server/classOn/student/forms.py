from wtforms import Form, StringField, PasswordField, validators, IntegerField, SelectField
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField

class PlaceSelectionForm(Form):
    row = IntegerField('Row', [validators.number_range(0)])
    column = IntegerField('Column', [validators.number_range(0)])