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

''' Flask app '''
app = Flask(__name__)

''' Global variables'''
global assigment_global

''' MySQL '''
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Oracle'
app.config['MYSQL_DB'] = 'classon'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)

''' Page routes and interactions '''
@app.route('/')
def index():
    return render_template('home.html')

# Register form class
class RegisterForm(Form):
    name = StringField('Nombre', [validators.Length(min = 1, max=100)])
    lastName = StringField('Apellido', [validators.Length(min = 1, max=100)])
    lastNameSecond = StringField('Segundo apellido', [validators.Length(min = 0, max=100)])
    nia = StringField('NIA', [validators.Length(min = 9, max=9)])
    email = StringField('Email', [validators.Length(min=1, max=100)])
    password = PasswordField('Contraseña',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Las contraseñas no coinciden')
    ])
    confirm = PasswordField('Confirm Password')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if(request.method == 'POST' and form.validate()):
        #Submited
        name = form.name.data
        lastName = form.lastName.data
        lastNameSecond = form.lastNameSecond.data
        nia = form.nia.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # DB access
        # Create the cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO students(name, last_name, last_name_second, NIA, email, password) VALUES(%s, %s, %s, %s, %s, %s)", (name, lastName, lastNameSecond, nia, email, password))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('You are now registerd and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        nia = request.form['nia']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute('SELECT * FROM students WHERE nia = %s', [nia])

        if (result > 0):
            # Get stored hash
            data = cur.fetchone()                   # Fetches the first one
            password = data['password']             # Dictionary

            # Compare passwords
            if (sha256_crypt.verify(password_candidate, password)):
                # Passed verification
                session['logged_in'] = True
                session['nia'] = nia
                session['progress'] = 1

                flash('You are now logged in', 'success')
                # $$$$ video minuto 15:49
                return redirect(url_for('Assigment'))

            else:
                error = 'Password Not matched'
                return render_template('login.html', error=error)
            # # Close connection
            # cur.close()
        else:
            app.logger.info('No user')
            error = 'NIA not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in                   # Uses the flask decorator to check if is logged in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

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

# Dashboard
@app.route('/assigment')
@is_logged_in                   # Uses the flask decorator to check if is logged in
def Assigment():
    global assigment_global                 # Used in this scope

    # Create cursor
    cur = mysql.connection.cursor()

    # Check if the global variable for assigment is loaded
    try:
        assigment_global
    except:
        assigment_global = setAssigment()

    # if (_assigment is None):
    #     _assigment = copy.deepcopy(setAssigment())

    if len(assigment_global.sections) > 0:
        progress = session['progress']
        return render_template(
            'assigment.html',
            assigment=assigment_global,
            progress=progress,
            section=assigment_global.sections_dict()[   progress]
        )

    ## Por debajo popó del programa anterior, pero vale de ejemplo
    ## Por debajo popó del programa anterior, pero vale de ejemplo
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall() # Dictionary
    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)
    #close connection
    cur.close()


''' Custom initialization at startup - Begin '''
app.debug = True
# manager = Manager(app)
#
# def custom_calls():
#     # setAssigment()
#     pass
#
# class CustomServer(Server):
#     def __call__(self, app, *args, **kwargs):
#         custom_calls()
#         app.secret_key = 'secret123'
#         # Hint: Here you could manipulate app
#         # - Threaded true allow multiple users
#         return Server.__call__(self, app, *args, **kwargs, threaded=True)
#
# # app = Flask(__name__)
#
# # Remember to add the command to your Manager instance
# manager.add_command('runserver', CustomServer())
#
# if __name__ == "__main__":
#     manager.run()          # Allow multiple users

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