from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import dataStructures

from classOn.decorators import is_logged_in
from classOn.home.forms import RegisterFormStudent, RegisterFormProfessor

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

    formStudent = RegisterFormStudent(request.form)
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

@home.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        email = ''
        password_candidate = ''
        isProfessor = False
        isStudent = False
        if request.form['btn'] == 'isStudent':
            email = request.form['email']
            password_candidate = request.form['password']
            isStudent = True
        elif request.form['btn'] == 'isProfessor':
            email = request.form['email']
            password_candidate = request.form['password']
            isProfessor = True
        else:
            raise IOError('login error')
            pass

        # Fetch from DB
        cur = mysql.connection.cursor()
        result = None
        if isStudent:
            result = cur.execute('SELECT * FROM students WHERE email = %s', [email])
        elif isProfessor:
            result = cur.execute('SELECT * FROM professors WHERE email = %s', [email])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()                   # Fetches the first one
            password = data['password']             # Dictionary

            # Compare passwords
            if (sha256_crypt.verify(password_candidate, password)):
                # Passed verification
                if isStudent:
                    session['logged_in'] = True
                    session['isProfessor'] = False
                    session['nia'] = data['NIA']
                    session['page'] = 1             # Assigment starts from first page

                    cur.close()                     # Close DB connection
                    flash('You are now logged in', 'success')
                    return redirect(url_for('assigment.Assigment_page', page=1))

                if isProfessor:
                    session['logged_in'] = True
                    session['isProfessor'] = True
                    session['id_professor'] = data['id']

                    cur.close()                     # Close DB connection
                    flash('You are now logged in professor', 'success')
                    return redirect(url_for('professor.index'))

            else:
                cur.close()                         # Close DB connection
                error = 'Password Not matched'
                return render_template('login.html', error=error)

        else:
            cur.close()
            error = 'email not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@home.route('/logout')
@is_logged_in                   # Uses the flask decorator to check if is logged in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home.login'))


