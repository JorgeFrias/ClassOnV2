from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from classOn.decorators import is_logged_in

'''Register blueprint'''
student = Blueprint('student',
                    __name__,
                    template_folder='templates',
                    static_folder='static'
                    )

''' Global objects import '''
from classOn import runningClasses


@student.route('/')
@is_logged_in
def index():
    return redirect(url_for('student.dashboard'))


@student.route('/dashboard')
@is_logged_in
def dashboard():
    # if there are classes to join:
    viewRuningClasses = {}
    if len(runningClasses) > 0:
        for id, runningClass in runningClasses.items():
            viewRuningClasses[id] = {'course': runningClass.assigment.course,
                                     'assigment': runningClass.assigment.name,
                                     'room': runningClass.room}

    return render_template('student_dashboard.html', runningClasses=viewRuningClasses)
