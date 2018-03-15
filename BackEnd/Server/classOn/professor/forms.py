from wtforms import Form, StringField, PasswordField, validators
from wtforms.widgets import TextArea

class CreateAssigmentForm(Form):
    course = StringField('Course', [validators.Length(min = 1, max=100)])
    name = StringField('Name', [validators.Length(min=1, max=100)])

class AddSectionForm(Form):
    name = StringField('Name', [validators.Length(min = 1, max=100)])
    text = StringField(u'Text', widget=TextArea())
