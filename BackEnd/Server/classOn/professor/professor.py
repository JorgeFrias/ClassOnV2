from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import dataStructures

from classOn.decorators import is_logged_in, is_logged_in_professor


'''Register blueprint'''
professor = Blueprint('professor',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql

@professor.route('/')
@is_logged_in_professor
def index():
    return redirect(url_for('professor.dashboard'))

@professor.route('/dashboard')
@is_logged_in_professor
def dashboard():
    return render_template('dashboard.html')