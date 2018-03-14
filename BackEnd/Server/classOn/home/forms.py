from wtforms import Form, StringField, PasswordField, validators

# Register form class
class RegisterFormStudent(Form):
    name = StringField('Nombre', [validators.Length(min = 1, max=100)])
    lastName = StringField('Apellido', [validators.Length(min = 1, max=100)])
    lastNameSecond = StringField('Segundo apellido', [validators.Length(min = 0, max=100)])
    nia = StringField('NIA', [validators.Length(min = 9, max=9)])
    email = StringField('Email', [validators.Length(min=1, max=100)])
    password = PasswordField('Contraseña',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Las contraseñas no coinciden')
    ])
    confirm = PasswordField('Confirm Password')

# Register form class
class RegisterFormProfessor(Form):
    name = StringField('Nombre', [validators.Length(min = 1, max=100)])
    lastName = StringField('Apellido', [validators.Length(min = 1, max=100)])
    lastNameSecond = StringField('Segundo apellido', [validators.Length(min = 0, max=100)])
    email = StringField('Email', [validators.Length(min=1, max=100)])
    password = PasswordField('Contraseña',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Las contraseñas no coinciden')
    ])
    confirm = PasswordField('Confirm Password')