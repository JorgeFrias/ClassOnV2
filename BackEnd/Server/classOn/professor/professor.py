from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import dataStructures

from classOn.decorators import is_logged_in


'''Register blueprint'''
home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

''' MySQL import '''
from classOn import mysql

