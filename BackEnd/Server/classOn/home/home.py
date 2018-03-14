from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import dataStructures

from classOn.decorators import is_logged_in


'''Register blueprint'''
home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql

''' Page routes and interactions '''
# Index
@home.route('/')
def index():
    return render_template('home.html')

# Register form class
class RegisterForm(Form):
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

def singInStudent(name, lastName, lastNameSecond, nia, email, password):
    # DB access
    # Create the cursor
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute(
        "INSERT INTO students(name, last_name, last_name_second, NIA, email, password) VALUES(%s, %s, %s, %s, %s, %s)",
        (name, lastName, lastNameSecond, nia, email, password))
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()

    flash('You are now registerd as student and can log in', 'success')

def singInProfessor(name, lastName, lastNameSecond, email, password):
    # DB access
    # Create the cursor
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute(
        "INSERT INTO professors(name, last_name, last_name_second, email, password) VALUES(%s, %s, %s, %s, %s)",
        (name, lastName, lastNameSecond, email, password))
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()

    flash('You are now registerd as professor and can log in', 'success')

# Register
@home.route('/register', methods=['GET', 'POST'])
def registerGeneral():

    formStudent = RegisterForm(request.form)
    formProfessor = RegisterFormProfessor(request.form)
    if (request.method == 'POST'):
        if request.form['btn'] == 'Submit student' and formStudent.validate():
            # flash('Student', 'success')
            singInStudent(
                formStudent.name.data,
                formStudent.lastName.data,
                formStudent.lastNameSecond.data,
                formStudent.nia.data,
                formStudent.email.data,
                sha256_crypt.encrypt(str(formStudent.password.data))
            )
            return redirect(url_for('home.login'))
        elif request.form['btn'] == 'Submit professor' and formProfessor.validate():
            # flash('Professor', 'success')
            singInProfessor(
                formProfessor.name.data,
                formProfessor.lastName.data,
                formProfessor.lastNameSecond.data,
                formProfessor.email.data,
                sha256_crypt.encrypt(str(formProfessor.password.data))
            )
            return redirect(url_for('home.login'))

    return render_template('register.html', formStudent=formStudent, formProfessor=formProfessor)


# # Register
# @home.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form)
#     if(request.method == 'POST' and form.validate()):
#         #Submited
#         name = form.name.data
#         lastName = form.lastName.data
#         lastNameSecond = form.lastNameSecond.data
#         nia = form.nia.data
#         email = form.email.data
#         password = sha256_crypt.encrypt(str(form.password.data))
#
#         # DB access
#         # Create the cursor
#         cur = mysql.connection.cursor()
#         # Execute query
#         cur.execute("INSERT INTO students(name, last_name, last_name_second, NIA, email, password) VALUES(%s, %s, %s, %s, %s, %s)", (name, lastName, lastNameSecond, nia, email, password))
#         # Commit to DB
#         mysql.connection.commit()
#         # Close connection
#         cur.close()
#
#         flash('You are now registerd and can log in', 'success')
#
#         return redirect(url_for('home.login'))
#
#     return render_template('register.html', form=form)

# User login
@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        nia = request.form['nia']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute('SELECT * FROM students WHERE nia = %s', [nia])

        if (result > 0):
            # Get stored hash
            data = cur.fetchone()                   # Fetches the first one
            password = data['password']             # Dictionary

            # Compare passwords
            if (sha256_crypt.verify(password_candidate, password)):
                # Passed verification
                session['logged_in'] = True
                session['nia'] = nia
                session['page'] = 1

                flash('You are now logged in', 'success')
                # $$$$ video minuto 15:49
                return redirect(url_for('assigment.Assigment_page', page=1))

            else:
                error = 'Password Not matched'
                return render_template('login.html', error=error)
            # # Close connection
            # cur.close()
        else:
            # home.logger.info('No user')
            error = 'NIA not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@home.route('/logout')
@is_logged_in                   # Uses the flask decorator to check if is logged in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home.login'))


