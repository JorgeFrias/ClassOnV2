from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import dataStructures
from classOn import DBUtils
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

# Register
@home.route('/register', methods=['GET', 'POST'])
def registerGeneral():

    formStudent = RegisterFormStudent(request.form)
    formProfessor = RegisterFormProfessor(request.form)
    if (request.method == 'POST'):
        if request.form['btn'] == 'Submit student' and formStudent.validate():
            # flash('student', 'success')
            DBUtils.putStudent(
                formStudent.name.data,
                formStudent.lastName.data,
                formStudent.lastNameSecond.data,
                formStudent.nia.data,
                formStudent.email.data,
                sha256_crypt.encrypt(str(formStudent.password.data))
            )
            flash('You are now registerd as student and can log in', 'success')
            return redirect(url_for('home.login'))
        elif request.form['btn'] == 'Submit professor' and formProfessor.validate():
            # flash('Professor', 'success')
            DBUtils.putProfessor(
                formProfessor.name.data,
                formProfessor.lastName.data,
                formProfessor.lastNameSecond.data,
                formProfessor.email.data,
                sha256_crypt.encrypt(str(formProfessor.password.data))
            )
            flash('You are now registerd as professor and can log in', 'success')
            return redirect(url_for('home.login'))

    return render_template('register.html', formStudent=formStudent, formProfessor=formProfessor)

@home.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        # Data structures to store the information
        student = None
        professor = None

        # Check the button pressed, and tries to fetch the information from DB
        if request.form['btn'] == 'isStudent':
            # Logging in as student
            email = request.form['email']
            password_candidate = request.form['password']
            student = DBUtils.getStudentBy_email(email)         # Load student information from DB if exists (None if not)
        elif request.form['btn'] == 'isProfessor':
            # Logging in as professor
            email = request.form['email']
            password_candidate = request.form['password']
            professor = DBUtils.getProfessorBy_email(email)     # Load professor information from DB if exists (None if not)
        else:
            flash('Error fetching user from DB', 'danger')
            raise IOError('login error')
            pass

        # Logging
        if student is not None:                     # Professor found
            if (sha256_crypt.verify(password_candidate, student.passwordHash)):         # Correct password
                # Session variables
                # Store information while the user is logged in
                session['logged_in'] = True
                session['isStudent'] = True         # Is a student
                session['page'] = 1                 # Assigment starts from first page
                session['db_id'] = student.db_id

                flash('You are now logged in', 'success')
                return redirect(url_for('student.index'))
            else:                                                                       # Incorrect password
                error = 'Password Not matched'
                return render_template('login.html', error=error)

        elif professor is not None:
            if (sha256_crypt.verify(password_candidate, professor.passwordHash)):         # Correct password
                # Session variables
                # Store information while the user is logged in
                session['logged_in'] = True
                session['isProfessor'] = True
                session['id_professor'] = professor.db_id

                flash('You are now logged in as professor', 'success')
                return redirect(url_for('professor.index'))
            else:                                                                       # Incorrect password
                error = 'Password Not matched'
                return render_template('login.html', error=error)

        else:
            error = 'Email not found'
            return render_template('login.html', error=error)

    # By default render Login template
    return render_template('login.html')

@home.route('/logout')
@is_logged_in                   # Uses the flask decorator to check if is logged in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home.login'))