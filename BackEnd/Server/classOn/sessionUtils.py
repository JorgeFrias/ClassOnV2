from flask import session
from dataStructures import Student, Professor

def studentLogIn(session : session, student : Student):
    set_isLoggedIn(session, True)
    set_isStudent(session, True)
    set_page(session, 1)                            # Assigment starts from first page
    set_student_id(session, student.db_id)

def professorLogIn(session : session, professor: Professor):
    set_isLoggedIn(session, True)
    set_isProfessor(session, True)
    set_professor_id(session, professor.db_id)

def logOut(session: session):
    session.clear()

def get_isStudent(session : session):
    return session['logged_in']
def set_isStudent(session : session, bool):
    session['logged_in'] = bool

def get_isProfessor(session : session):
    return session['isStudent']
def set_isProfessor(session : session, bool):
    session['isProfessor'] = bool


'''   Variable extraction  '''
def get_isLoggedIn(session : session):
    return session['logged_in']
def set_isLoggedIn(session : session, bool):
    session['logged_in'] = bool

def get_professor_id(session : session):
    return session['id_professor']
def set_professor_id(session : session, id):
    session['id_professor'] = id

def get_assigment_id(session : session):
    return session['id_assigment']
def set_assigment_id(session : session, id):
    session['id_assigment'] = id

def get_orderInAssigment(session : session):
    return session['order_in_assigment']
def set_orderInAssigment(session : session, id):
    session['order_in_assigment'] = id
def increment_orderInAssigment(session : session):
    session['order_in_assigment'] += 1

def get_class_id(session : session):
    return session['id_class']
def set_class_id(session : session, id):
    session['id_class'] = id

def get_grupo_id(session : session):
    return session['group_id']
def set_grupo_id(session : session, id):
    session['group_id'] = id

def get_student_id(session: session):
    return session['db_id']
def set_student_id(session : session, id):
    session['db_id'] = id

def get_page(session: session):
    return session['page']
def set_page(session: session, page):
    session['page'] = page

def set_socketioConected(bool : bool):
    session['socket_io'] = bool
def get_socketioConected():
    return session['socket_io']
