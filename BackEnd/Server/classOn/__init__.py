from flask import Flask, redirect, url_for

''' Flask application '''
app = Flask(__name__, instance_relative_config=True)

''' Configurations '''
# Load the default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')
# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

''' Database '''
from flask_mysqldb import MySQL
mysql = MySQL(app)

''' Socket.io '''
from flask_socketio import SocketIO, emit
socketio = SocketIO(app)

''' Global information '''
from dataStructures import Classroom
runningClasses = {}

''' Blueprints - register '''
from classOn.home.home import home
from classOn.assigment.assigment import assigment
from classOn.professor.professor import professor
from classOn.student.student import student
app.register_blueprint(home)
app.register_blueprint(assigment, url_prefix='/assigment')
app.register_blueprint(professor, url_prefix='/professor')
app.register_blueprint(student, url_prefix='/student')


''' Routing '''
@app.route('/')
def index():
    return redirect(url_for('home.index'))
