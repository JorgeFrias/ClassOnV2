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

''' Blueprints - register '''
from classOn.home.home import home
from classOn.assigment.assigment import assigment
app.register_blueprint(home)
app.register_blueprint(assigment, url_prefix='/assigment')

''' Routing '''
@app.route('/')
def index():
    return redirect(url_for('home.index'))
