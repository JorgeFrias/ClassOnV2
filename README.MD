# ClassOn V2
## Description
This is a class management application for professors. The students can see a assignment text ant the professor can check the progress of the students for the given assignment. Students can post doubts, the professor is offered a list of waiting groups with doubts so he can answer in a given order.

## Installation

## Usage
In order to run the code you need to execute the app.py script with ``runserver`` command.  

Once the code is running you can go to the deployment address of the system and use it.

### Configuration before running
Before you'll have to:
1. Install all code dependences specified in ````requiriments.txt```` file.
2. Config the DB running the SQL scripts inside ````MySQL_schema```` in order to have the schema.
3. Config the DB connection credentials (steps specified in DB section).

### Professor 
1. Logs in.
2. Creates a classroom for a given assignment, with a fixed size, and a given room.
3. It's redirected to a page where the professor can see the seats which students are in which place, the progress in the assignment, the doubts they have, and the solutions to the doubt from the students.

The professor can also upload assignment after be logged in.

### Student
1. Logs in.
2. Selects one of the running sessions.
3. Gets the assignment. He can see the different pages, upload doubts and solve doubts from others.

## Developer guide  
The system it's based on [Flask server](http://flask.pocoo.org), it's a microframework python based to serve pages built in the server. 
Also uses JavaScript and [Socket.io](https://socket.io) to communicate when no refreshing is allowed, well a special version designed to work with [flask](http://flask-socketio.readthedocs.io/en/latest/).

The project uses a structure of folders with a folder for each page or section of pages with common responsibilities. 

```
├───classOn  
│   DBUtils.py  
│   decorators.py  
│   models.py  
│   sessionUtils.py 
│   __init__.py
├───assigment
│   │   assigment.py
│   │   forms.py
│   │   __init__.py
│   │
│   ├───static
│   │   └───js
│   │           script_assigment.js
│   └───templates
│           assigment.html
│           doubt.html
│           modal.html
├───home
│   │   forms.py
│   │   home.py
│   │   __init__.py
│   └───templates
│           home.html
│           login.html
│           loginProfessor.html
│           loginStudent.html
│           register.html
│           registerProfessor.html
│           registerStudent.html
├───professor
│   │   forms.py
│   │   professor.py
│   │   __init__.py
│   │
│   ├───static
│   │   └───js
│   │           script.js
│   └───templates
│           addSections.html
│           classroomMap.html
│           createAssigment.html
│           createClassroom.html
│           dashboard.html
├───student
│   │   forms.py
│   │   student.py
│   │   __init__.py
│   └───templates
│           selectPlace.html
│           student_dashboard.html
└───templates
    │   layout.html
    └───includes
            _formhelpers.html
            _generalScripts.html
            _messages.html
            _navbar.html
```

The various python files under a folder defines the logic estructure and algorithims ClassOn follows. The file structure uses [flask blueprints](http://flask.pocoo.org/docs/1.0/blueprints/) intended to give a better structure to a complex system.

There are two types of user professor and student. The pages they can acess are diferent.
- Professor
    - Home
    - Professor
- Student 
    - Home
    - Assignment
    - Student

The decorator ``@assigment.route()`` is used to define pages to serve with a defined route, so page refresh is needed.

The decorator ``@socketio.on()`` is used to attend to socket events, when is used no page refresh is needed. This functions allows communication between the server an the client dynamically.

### Database
The system uses an [MySQL](https://www.mysql.com) database, the libraries are wrote to use MySQL database. In order to migrate to another DB is needed to modify just DBUtils.py.  

In order to connect to you DB instance you need a config file inside config folder. You can name the file as you want. For example ```development.py``` you will have to fulfill al the fields required with the connection information.

````
SECRET_KEY = 'your key'
MYSQL_HOST = 'your host'
MYSQL_USER = 'your user'
MYSQL_PASSWORD = 'your pass'
MYSQL_DB = 'my DB instance, just kidding your DB instance'
MYSQL_CURSORCLASS = 'your cursor class'
````
[Check here for more information](http://flask-mysqldb.readthedocs.io/en/latest/).
And use the command in order to run it for debugging you have to use the command ``PYTHONUNBUFFERED=1;APP_CONFIG_FILE=C:\*Your Route*\ClassOnV2\BackEnd\Server\config\development.py``

If you want to debug the code (in pycharm for example) you'll have to add a new line with ````DEBUG = True````.

### Front 
The system it's based on [Bootstrap 4](https://getbootstrap.com), which makes the pages generated responsive easily.