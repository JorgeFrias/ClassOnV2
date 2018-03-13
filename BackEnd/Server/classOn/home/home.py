from flask import Blueprint, render_template
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_script import Manager, Server
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
import dataStructures


'''Register blueprint'''
home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from app import mysql

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

# Register
@home.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if(request.method == 'POST' and form.validate()):
        #Submited
        name = form.name.data
        lastName = form.lastName.data
        lastNameSecond = form.lastNameSecond.data
        nia = form.nia.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # DB access
        # Create the cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO students(name, last_name, last_name_second, NIA, email, password) VALUES(%s, %s, %s, %s, %s, %s)", (name, lastName, lastNameSecond, nia, email, password))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('You are now registerd and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

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
                return redirect(url_for('Assigment_page', page=1))

            else:
                error = 'Password Not matched'
                return render_template('login.html', error=error)
            # # Close connection
            # cur.close()
        else:
            home.logger.info('No user')
            error = 'NIA not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@home.route('/logout')
@is_logged_in                   # Uses the flask decorator to check if is logged in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

def setAssigment():
    # global assigment_global                 # Used in this scope
    DB_Assigment = None
    cur = mysql.connection.cursor()
    assig_query = cur.execute("SELECT * FROM assigments")
    #close connection
    if assig_query > 0:
        # Just get's one supports just one assigment in DB
        assig = cur.fetchone()                       # Dictionaty
        # Get sections
        id = assig['id']
        sections_query = cur.execute("SELECT * FROM sections WHERE assigment = %s", [id])
        if sections_query > 0:
            tmpSections = []
            sections = cur.fetchall()
            for section in sections:
                tmpSection = dataStructures.Section(
                    section['title'],
                    section['order_in_assigment'],
                    section['content']
                )
                tmpSections.append(tmpSection)
            DB_Assigment = dataStructures.Assigment(tmpSections, assig['course'])

    cur.close()
    # _assigment = copy.deepcopy(DB_Assigment)
    return DB_Assigment
