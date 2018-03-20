from flask import render_template, flash, redirect, url_for, session, request, Blueprint
import dataStructures
from classOn import DBUtils
from classOn.decorators import is_logged_in_professor
from classOn.professor import forms
import uuid

'''Register blueprint'''
professor = Blueprint('professor',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql

''' Global objects import '''
from classOn import runningClasses

@professor.route('/')
@is_logged_in_professor
def index():
    return redirect(url_for('professor.dashboard'))

@professor.route('/dashboard')
@is_logged_in_professor
def dashboard():
    return render_template('dashboard.html')

@professor.route('/create_assigment', methods=['GET', 'POST'])
@is_logged_in_professor
def createAssigment():

    form = forms.CreateAssigmentForm(request.form)

    if (request.method == 'POST' and form.validate()):
        cur = mysql.connection.cursor()

        course = form['course'].data
        name = form['name'].data
        id_professor = session['id_professor']

        # Execute query
        cur.execute(
            "INSERT INTO assigments(name, course, id_professor) VALUES(%s, %s, %s)",
            (name, course, id_professor))
        mysql.connection.commit()                           # Commit to DB
        session['id_assigment'] = cur.lastrowid             # Store id to add sections
        session['order_in_assigment'] = 0                   # To be in control adding sections
        cur.close()                                         # Close connection

        flash('You created a new assigment', 'success')

        return redirect(url_for('professor.addSections', course=course, name=name))

    return render_template('createAssigment.html', form=form)

def fetchSections(id_assigment):
    sections = []
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM sections WHERE id_assigment = %s', [id_assigment])
    if result > 0:
        # data = cur.fetchone()  # Fetches the first one
        # Using the cursor as iterator
        for row in cur:
            tmpSection = dataStructures.Section(row['name'], row['order_in_assigment'], row['text'])
            sections.append(tmpSection)

    return sections

@professor.route('/add_sections', methods=['GET', 'POST'])
@is_logged_in_professor
def addSections():
    form = forms.AddSectionForm(request.form)

    if (request.method == 'POST' and form.validate()):
        if request.form['btn'] == 'add' or request.form['btn'] == 'addFinish':
            session['order_in_assigment'] += 1  # Update order

            id_assigment = session['id_assigment']
            order_in_assigment = session['order_in_assigment']
            name = form['name'].data
            text = form['text'].data

            # Execute query
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO sections(id_assigment, order_in_assigment, name, text) VALUES(%s, %s, %s, %s)",
                (id_assigment, order_in_assigment, name, text))
            mysql.connection.commit()           # Commit to DB
            cur.close()                         # Close connection

            if request.form['btn'] == 'add':
                return redirect(url_for('professor.addSections'))
            elif request.form['btn'] == 'addFinish':
                flash('Saved', 'success')
                return redirect(url_for('professor.dashboard'))
            else:
                flash('Something uncontrolled append', 'danger')
                return redirect(url_for('professor.dashboard'))

        elif request.form['btn'] == 'cancel':
            flash('Discarded last section', 'danger')
            flash('Saved all others', 'success')
            return redirect(url_for('professor.dashboard'))
        else:
            flash('Something uncontrolled append', 'danger')
            return redirect(url_for('professor.dashboard'))

    ### Fetch info to render ###
    order_in_assigment = session['order_in_assigment'] + 1      # Do not update here because user can reload the page
    # Fetch sections to render
    # sections = fetchSections(session['id_assigment'])           # Get sections
    sections = DBUtils.getSections(session['id_assigment'])     # Get sections
    tmpAssigment = dataStructures.Assigment(sections)           # Create a temporal
    dicSections = tmpAssigment.sections_dict()                  # Create dict from temporal to render later

    return render_template('addSections.html', form=form, order_in_assigment=order_in_assigment, sections=dicSections)

def assigmentsTupleList(id_professor):
    '''
    Creates a list of tuples (id, title) for the assigments of the current professor (session['id_professor']
    '''
    assigments = []
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM assigments WHERE id_professor = %s', [id_professor])
    if result > 0:
        # data = cur.fetchone()  # Fetches the first one
        # Using the cursor as iterator
        for row in cur:
            tmpTuple = (row['id'], row['name'])
            # assigments[row['id']] = row['name']
            assigments.append(tmpTuple)

    return assigments

@professor.route('/create_classroom', methods=['GET', 'POST'])
@is_logged_in_professor
def createClassroom():
    form = forms.CreateClassroom(request.form)

    # Dynamic drop-down menu to choose the available assigments for professor
    assigments = assigmentsTupleList(session['id_professor'])
    form.assigment.choices = assigments

    if (request.method == 'POST' and form.validate()):
        # Form information about the new classroom
        rows = form['rows'].data
        columns = form['columns'].data
        room = form['room'].data
        selectedAssigmentID = form['assigment'].data

        # Classroom objects initialization
        assigmentObj = DBUtils.getAssigment(selectedAssigmentID)                                            # Object assigment
        currentProfessor = DBUtils.getProfessor(session['id_professor'])                                    # Object professor
        classroom = dataStructures.Classroom((rows,columns), currentProfessor, assigmentObj, room)   # Object ClassRoom

        id = str(uuid.uuid4())              # Classroom Universally Unique IDentifier (UUID) URN Namespace
        runningClasses[id] = classroom      # Add to runningClasses with id to be able to track different courses

        session['id_class'] = id            # Add to professor's session

        # Messages
        flash('Classroom created for assigment id = ' + str(selectedAssigmentID), 'success')
        flash('Internal classroom id = '+ str(id), 'success')

        return redirect(url_for('professor.dashboard'))

    return render_template('createClassroom.html', form=form)