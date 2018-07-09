from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import dataStructures
from classOn import DBUtils
from classOn.decorators import is_logged_in, is_in_group
from classOn.home.forms import RegisterFormStudent, RegisterFormProfessor
from classOn import sessionUtils as su
from classOn import accessController as ac
from classOn import runningClasses
from classOn.student import student as StudentClass
from classOn import DBUtils
from classOn import socketio



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
        studentPasswordIncorrect = None
        professorPasswordIncorrect = None

        # Check the button pressed, and tries to log in
        if request.form['btn'] == 'isStudent':
            studentPasswordIncorrect = ac.access.loginStudent(request,session)

        elif request.form['btn'] == 'isProfessor':
            professorPasswordIncorrect = ac.access.loginProfessor(request, session)

        else:
            flash('Error', 'danger')
            raise IOError('login error')
            pass

        # Logging
        if studentPasswordIncorrect is not None:                        # Professor found
            if (not studentPasswordIncorrect):                          # Correct password
                flash('You are now logged in', 'success')
                return redirect(url_for('student.index'))
            else:                                                       # Incorrect password
                error = 'Password Not matched'
                return render_template('login.html', error=error)

        elif professorPasswordIncorrect is not None:
            if (not professorPasswordIncorrect):                        # Correct password

                flash('You are now logged in as professor', 'success')
                return redirect(url_for('professor.index'))
            else:                                                       # Incorrect password
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
    # Cleaning procedures
    selectedRunningClass = runningClasses[su.get_class_id(session)]
    groupIsIn = selectedRunningClass.studentGroups[su.get_grupo_id(session)]

    # Delete the group from the memory
    del selectedRunningClass.studentGroups[su.get_grupo_id(session)]
    # Notify to the professor the changes
    removeGroup(groupIsIn)

    su.logOut(session)
    flash('You are now logged out', 'success')
    return redirect(url_for('home.login'))

def removeGroup(group):
    currentClass = runningClasses[su.get_class_id(session)]
    # stateJson = currentClass.JSON()
    room = su.get_classRoom(session)
    socketio.emit('removeGroup', group.JSON(), room=room)

@home.route('/add_new_member', methods=['GET', 'POST'])
@is_logged_in
@is_in_group
def addNewMember():
    if (request.method == 'POST'):
        # Data structures to store the information
        studentPasswordIncorrect = None

        # Check the button pressed, and tries to log in
        if request.form['btn'] == 'isStudent':
            studentPasswordIncorrect = ac.access.loginStudent(request, session)
        else:
            flash('Error', 'danger')
            raise IOError('login error')
            pass

        # Logging
        if studentPasswordIncorrect is not None:                        # Professor found
            if (not studentPasswordIncorrect):                          # Correct password
                flash('You are now logged in', 'success')
                # Success now join the desired group
                selectedRunningClass = runningClasses[su.get_class_id(session)]
                groupIsIn = selectedRunningClass.studentGroups[su.get_grupo_id(session)]
                studentid = su.get_students_id_group(session)[-1]         # last student to join the group
                student = DBUtils.getStudentBy_id(studentid)
                selectedRunningClass.addStudentToPlace(student, groupIsIn.positionInClass)

                # Redirect for assigment page
                assigmentID = selectedRunningClass.assigment.db_id  # Current assigment id

                ''' Socket.io notification'''
                StudentClass.handle_joinGroup(groupIsIn)

                # Render de selected assigment at the start page
                return redirect(url_for('assigment.assigmentByID', id=assigmentID, page=su.get_page(session)))

            else:                                                       # Incorrect password
                error = 'Password Not matched'
                return render_template('login.html', error=error)

        else:
            error = 'Email not found'
            return render_template('login.html', error=error)

    # By default render Login template
    return render_template('appendStudent.html')