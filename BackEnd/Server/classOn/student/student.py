from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from classOn.decorators import is_logged_in
from classOn import DBUtils

'''Register blueprint'''
student = Blueprint('student',
                    __name__,
                    template_folder='templates',
                    static_folder='static'
                    )

''' Global objects import '''
from classOn import runningClasses
from classOn.student import forms

@student.route('/')
@is_logged_in
def index():
    return redirect(url_for('student.dashboard'))

@student.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():

    if request.method == 'POST':
        runningClassID = 0
        if "btn" in request.form:                               # Some running class is selected
            runningClassID = request.form['btn']                # Get the id
            session['runningClassID'] = runningClassID          # Store in session

            return redirect(url_for('student.selectPlace'))     # Go to select place

    # if there are classes to join:
    viewRuningClasses = {}
    if len(runningClasses) > 0:
        for id, runningClass in runningClasses.items():
            viewRuningClasses[id] = {'course': runningClass.assigment.course,
                                     'assigment': runningClass.assigment.name,
                                     'room': runningClass.room,
                                     'assigment_id': runningClass.assigment.db_id}



    return render_template('student_dashboard.html', runningClasses=viewRuningClasses)

@student.route('/select_place', methods=['GET', 'POST'])
@is_logged_in
def selectPlace():
    form = forms.PlaceSelectionForm(request.form)

    if (request.method == 'POST' and form.validate()):
        # Get running classroom instance
        selectedRunningClass = runningClasses[session['runningClassID']]
        rows = selectedRunningClass.classSize[0]
        cols = selectedRunningClass.classSize[1]

        # Form info
        row = form['row'].data
        column = form['column'].data

        # Check if is out of bounds
        if (row <= rows and column <= cols):
            # Inside of bounds. The student can take the seat.
            student = DBUtils.getStudentBy_id(session['db_id'])                             # Generate student
            groupIsIn = selectedRunningClass.addStudentToPlace(student, (row, column))      # Add to selected class
            session['group_id'] = groupIsIn.groupID                                         # Store id as reference

            flash('Place selected', 'success')

            assigmentID = selectedRunningClass.assigment.db_id                              # Current assigment id
            startPage = 0 # If there is already an student?

            return redirect(url_for('assigment.assigmentByID', id= assigmentID, page=startPage))
            # Go to assigment
        else:
            flash('Place out of bounds', 'danger')
            return redirect(url_for('student.selectPlace'))


    return render_template('selectPlace.html', form=form)
