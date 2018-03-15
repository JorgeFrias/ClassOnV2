from wtforms import Form, StringField, PasswordField, validators
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField

class CreateAssigmentForm(Form):
    course = StringField('Course', [validators.Length(min = 1, max=100)])
    name = StringField('Name', [validators.Length(min=1, max=100)])

class AddSectionForm(Form):
    name = StringField('Name', [validators.Length(min = 1, max=100)])
    # text = StringField(u'Text', widget=TextArea())
    text = TextAreaField('Text', render_kw={"rows": 15  })
    # text = TextAreaField(u'Text')

