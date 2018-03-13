from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import dataStructures
from classOn.decorators import is_logged_in

'''Register blueprint'''
assigment = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql

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

@assigment.route('/assigment/<string:page>', methods=['GET', 'POST'])
@is_logged_in                   # Uses the flask decorator to check if is logged in
def Assigment_page(page):
    global assigment_global                 # Used in this scope
    page_no = int(page)
    # Create cursor
    cur = mysql.connection.cursor()

    # Check if the global variable for assigment is loaded
    try:
        assigment_global
    except:
        assigment_global = setAssigment()

    # If zero last one visited in session
    if page_no == 0:
        # Render last visited
        page_no = session['page']
    else:
        #Update session
        session['page'] = page_no

    totalSections = len(assigment_global.sections)
    progress = ProgressPercentaje(page_no, totalSections)
    if  totalSections > 0:
        if page_no > 0 and page_no <= len(assigment_global.sections):
            # The requested page exists
            # progress = session['progress']
            return render_template(
                'assigment.html',
                assigment=assigment_global,
                progress=progress,
                page=page_no,
                totalSections=totalSections,
                section=assigment_global.sections_dict()[page_no - 1]
            )
        else:
            # Error
            flash('Requested page out of bounds', 'danger')
    else:
        # Error
        flash('No sections in current assigment', 'danger')

def ProgressPercentaje(currentPage, totalPages):
    return 100/totalPages * currentPage