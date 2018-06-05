from flask import render_template, flash, redirect, url_for, session, request, Blueprint
# from wtforms import Form, StringField, PasswordField, validators
# from passlib.hash import sha256_crypt
# from functools import wraps
from dataStructures import Doubt, Section, Assigment
from classOn.decorators import is_logged_in
from classOn import DBUtils
from classOn import sessionUtils as su
from classOn.assigment import forms
from classOn import sessionUtils as su
from flask_socketio import SocketIO, join_room, leave_room

'''Register blueprint'''
assigment = Blueprint('assigment',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql
from classOn import runningClasses
from classOn import socketio
from dataStructures import StudentGroup

def setAssigment():
    # global assigment_global                       # Used in this scope
    DB_Assigment = None
    cur = mysql.connection.cursor()
    assig_query = cur.execute("SELECT * FROM assigments")
    #close connection
    if assig_query > 0:
        # Just get's one supports just one assigment in DB
        assig = cur.fetchone()                       # Dictionary
        # Get sections
        id = assig['id']
        sections_query = cur.execute("SELECT * FROM sections WHERE assigment = %s", [id])
        if sections_query > 0:
            tmpSections = []
            sections = cur.fetchall()
            for section in sections:
                tmpSection = Section(
                    section['id'],
                    section['title'],
                    section['order_in_assigment'],
                    section['content']
                )
                tmpSections.append(tmpSection)
            DB_Assigment = Assigment(tmpSections, assig['course'])

    cur.close()
    return DB_Assigment

def ProgressPercentaje(currentPage, totalPages):
    return 100/totalPages * currentPage

@assigment.route('/<string:id>/<string:page>', methods=['GET', 'POST'])
@is_logged_in                                               # Uses the flask decorator to check if is logged in
def assigmentByID(id, page):
    page_no = int(page)                                     # Conversion to int
    assigment = DBUtils.getAssigment(id)                    # Get requested assigment (db_id -> id)
    currentClass = runningClasses[su.get_class_id(session)]
    currentGroup = currentClass.studentGroups[su.get_grupo_id(session)]

    form = forms.PostDoubtForm(request.form)

    ## DOUBT ###
    ### $$$$ Falla porque recarga la página. hay que hacer esto sin recargarla.
    # if (request.method == 'POST' and form.validate()):
    #
    #     doubtText = form['text'].data
    #     form['text'].data = ''                              # Clear
    #     doubt = Doubt(doubtText, currentClass.assigment.sections[page_no - 1], currentGroup)
    #     doubt.postToDB()
    #     currentClass.doubts.append(doubt)
    #     currentGroup.doubts.append(doubt)
    #
    #     flash('Doubt sent', 'success')
    #
    #     # Notify to Professor and Students
    #     handle_newDoubt(doubt)


    if assigment is None:
        # Doesn't exist an assigment with the requested id
        flash('Doesn\'t exists an assigment with id: ' + str(id) , 'danger')
    else:
        # If zero last one visited in session
        if page_no == 0:
            page_no = su.get_page(session)                  # Render last visited
        else:
            su.set_page(session, page_no)                   # Update session
            currentGroup.assigmentProgress = page_no        # Update group obj

        totalSections = len(assigment.sections)
        progress = ProgressPercentaje(page_no, totalSections)

        if totalSections > 0:
            if page_no > 0 and page_no <= len(assigment.sections):
                # The requested page exists
                updateGroupAssigmentProgress(su.get_grupo_id(session), page_no)     # Notify
                return render_template(
                    'assigment.html',
                    assigment=assigment,
                    progress=progress,
                    page=page_no,
                    totalSections=totalSections,
                    section=assigment.sections_dict()[page_no - 1],  # -1 Because the computer starts counting at 0
                    form = form
                )
            else:
                # Error
                flash('Requested page out of bounds', 'danger')
        else:
            # Error
            flash('No sections in current assigment', 'danger')

''' SOCKET.IO '''
@socketio.on('updateCredentials')
def handle_connection():
    selectedRunningClass = runningClasses[su.get_class_id(session)]
    su.set_classRoom(session, selectedRunningClass.id)
    su.set_ownRoom(session, request.sid)
    join_room(selectedRunningClass.id)

def updateGroupAssigmentProgress(groupID, progress):
    '''
    Updates the assigment progress to all the interested.
    IMPROVE: In order to improve this, we can create groups to send the info only to interested clients.
    :param groupID:
    :param progress:
    :return:
    '''
    selectedRunningClass = runningClasses[su.get_class_id(session)]
    currentGroup = selectedRunningClass.studentGroups[su.get_grupo_id(session)]
    currentGroup.assigmentProgress = progress
    su.set_classRoom(session, selectedRunningClass.id)
    handle_assigmentChangePage(currentGroup)

def handle_assigmentChangePage(group : StudentGroup):
    room = su.get_classRoom(session)
    socketio.emit('assigment_changeProgress', group.JSON(), room=room)

@socketio.on('doubt_post')
def handle_postDoubt(text):
    '''
    New doubt from a student. Stores the doubt in the system and send it to all other students
    :param text:
    :return:
    '''
    currentClass = runningClasses[su.get_class_id(session)]
    currentGroup = currentClass.studentGroups[su.get_grupo_id(session)]
    page_no = currentGroup.assigmentProgress

    doubtText = text
    doubt = Doubt(doubtText, currentClass.assigment.sections[page_no - 1], currentGroup)
    doubt.postToDB()
    currentClass.addDoubt(doubt)
    currentGroup.doubts.append(doubt)

    flash('Doubt sent', 'success')

    # Notify to Professor and Students
    room = su.get_classRoom(session)
    socketio.emit('doubt_new', doubt.JSON(), room=room)

@socketio.on('doubt_query')
def hadle_queryDoubts():
    currentClass = runningClasses[su.get_class_id(session)]
    # doubtsJson = '{"doubts":['
    # for doubt in currentClass.doubts:
    #     doubtsJson += doubt[1].JSON() + ','
    # if (len(currentClass.doubts) > 0):
    #     doubtsJson = doubtsJson[:-1]                                    # Remove last comma
    # doubtsJson += "]}"

    doubtsJson = currentClass.JSON()

    room = su.get_ownRoom(session)                                  # Who asked for doubts

    print('Doubt query to: ' + room)
    socketio.emit('doubt_query_result', doubtsJson, room=room)

@socketio.on('answer_post')
def handle_answerPost(doubtId, answer):
    # $$$$ Professors are not supported to solve doubts
    currentClass = runningClasses[su.get_class_id(session)]
    solvedDoubt = currentClass.getDoubt(doubtId)                    # We are using variables in memory
    # solvedDoubt = DBUtils.getDoubt(int(doubtId))
    solver = DBUtils.getStudentBy_id(su.get_student_id(session))    # Student solver

    # Update memory currentClass.doubts
    solvedDoubt.add_Answer(answer, solver)                          # Do not use DBUtils.
    # DBUtils.answerDoubt(solvedDoubt, answer, solver)

    answerJson = '{"doubtid":' + str(doubtId) + ',' +\
                 '"text":"' + answer + '"}'
    room = su.get_classRoom(session)
    socketio.emit('new_answer', answerJson, room=room)
