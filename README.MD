# To do:  
- [ ] Write a great ReadMe.  
- [ ] Commit great ReadMe.  

Project name: Your project’s name is the first thing people will see upon scrolling down to your README, and is included upon creation of your README file.

# ClassOn V2
## Description
This is a class management application for professors. The students can see a assignment text ant the professor can check the progress of the students for the given assignment. Students can post doubts, the professor is offered a list of waiting groups with doubts so he can answer in a given order.

## Installation

## Usage
### Professor 
1. Logs in.
2. Creates a classroom for a given assigment, with a fixed size, and a given room.
3. It's redirected to a page where the professor can see the seats whith which estudents are in which place, the progress in the assigment, the doubts they have, and the solutions to the doubt from the students.

The professor can also upload assigments after be logged in.

### Student
1. Logs in.
2. Selects one of the running sessions.
3. Gets the assigment. He can see the different pages, upload doubts and solve doubts from others.

## Developer guide  
The system it's based on [Flask server](http://flask.pocoo.org), it's a microframework python based to serve pages built in the server. 
Also uses JavaScript and [Socket.io](https://socket.io) to comunicate when no refreshing is allowed, well a special version desinged to work with [flask](http://flask-socketio.readthedocs.io/en/latest/).

The project uses a structure of folders with a folder for each page or section of pages with common responsabilities. 

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
    - Assigment
    - Student

The decorator ``@assigment.route()`` is ussed to define pages to serve with a defined route, so page refresh is needed.

The decorator ``@socketio.on()`` is ussed to attend to socket events, when is used no page refresh is needed. This functions allows comunication between the server an the client dynamicaly.

### Database
The system uses an [MySQL](https://www.mysql.com) database, the libraries are wrote to use MySQL databse. In order to migrate to another DB is needed to modify just DBUtils.py.  

### Front 
The system it's based on [Bootstrap 4](https://getbootstrap.com), which makes the pages generated responsive eassily.