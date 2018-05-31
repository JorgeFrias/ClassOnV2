from wtforms import Form, StringField, PasswordField, validators, IntegerField, SelectField
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField


class PostDoubtForm(Form):
    # name = StringField('Name', [validators.Length(min = 1, max=100)])
    # text = StringField(u'Text', widget=TextArea())
    text = TextAreaField('New doubt:', render_kw={"rows": 5  })