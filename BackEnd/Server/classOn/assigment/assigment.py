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


'''Register blueprint'''
assigment = Blueprint('assigment',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql
from classOn import runningClasses

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
@is_logged_in                                       # Uses the flask decorator to check if is logged in
def assigmentByID(id, page):
    page_no = int(page)                             # Conversion to int
    assigment = DBUtils.getAssigment(id)            # Get requested assigment (db_id -> id)

    form = forms.PostDoubtForm(request.form)

    if (request.method == 'POST' and form.validate()):
        currentClass = runningClasses[su.get_class_id(session)]
        currentGroup = currentClass.studentGroups[su.get_grupo_id(session)]

        doubtText = form['text'].data
        doubt = Doubt(doubtText, currentClass.assigment.sections[page_no - 1], currentGroup)
        currentClass.doubts.append(doubt)
        currentGroup.doubts.append(doubt)

        # Notify code, to refresh views



    if assigment is None:
        # Doesn't exist an assigment with the requested id
        flash('Doesn\'t exists an assigment with id: ' + str(id) , 'danger')
    else:
        # If zero last one visited in session
        if page_no == 0:
            page_no = su.get_page(session)          # Render last visited
        else:
            su.set_page(session, page_no)           # Update session

        totalSections = len(assigment.sections)
        progress = ProgressPercentaje(page_no, totalSections)

        if totalSections > 0:
            if page_no > 0 and page_no <= len(assigment.sections):
                # The requested page exists
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
