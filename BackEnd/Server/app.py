from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_script import Manager, Server
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
# from DataStructures import assigment, Section
import dataStructures
import copy

# ''' Flask app '''
# app = Flask(__name__)
#
# ''' Global variables'''
# global assigment_global
#
# ''' MySQL '''
# # Config MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Oracle'
# app.config['MYSQL_DB'] = 'classon'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
# mysql = MySQL(app)

# ''' Page routes and interactions '''
# @app.route('/')
# def index():
#     return render_template('home.html')


'''
Pages start at 1
if 0 render last one visited
'''


''' Custom initialization at startup - Begin '''
# app.debug = True

import app

# No debug with pycharm
if __name__ == '__main__':
    # _assigment = setAssigment()         # Set the assigment
    app.secret_key = 'secret123'
    # app.run(threaded=True)              # Allow multiple users
    app.run()              # Allow one user

# Debug with pycharm
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)

''' Custom initialization at startup - End '''