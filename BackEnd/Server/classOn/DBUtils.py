from dataStructures import Assigment, Section, Professor, Student, Doubt, StudentGroup

''' MySQL import '''
from classOn import mysql

def putStudent(name, lastName, lastNameSecond, nia, email, password):
    # DB access
    # Create the cursor
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute(
        "INSERT INTO students(name, last_name, last_name_second, NIA, email, password) VALUES(%s, %s, %s, %s, %s, %s)",
        (name, lastName, lastNameSecond, nia, email, password))

    mysql.connection.commit()       # Commit to DB
    id = cur.lastrowid              # DB row id
    cur.close()                     # Close connection
    return id

def putProfessor(name, lastName, lastNameSecond, email, password):
    # DB access
    # Create the cursor
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute(
        "INSERT INTO professors(name, last_name, last_name_second, email, password) VALUES(%s, %s, %s, %s, %s)",
        (name, lastName, lastNameSecond, email, password))

    mysql.connection.commit()       # Commit to DB
    id = cur.lastrowid              # DB row id
    cur.close()                     # Close connection
    return id

def getProfessor(id):
    professor = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM professors WHERE id = %s', [id])
    if result > 0:
        data = cur.fetchone()  # Fetches the first one "should be just one"
        professor = Professor(id, data['name'], data['last_name'], data['last_name_second'], data['email'])
    else:
        raise RuntimeError('No assigment with id: ' + str(id))
        pass

    cur.close()
    return professor

def getStudentBy_id(id):
    student = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM students WHERE id = %s', [id])
    if result > 0:
        data = cur.fetchone()  # Fetches the first one "should be just one"
        student = Student(id, data['NIA'], data['name'], data['last_name'],
                          data['last_name_second'], data['email'], data['password'])
    else:
        raise RuntimeError('No assigment with id: ' + str(id))
        pass

    cur.close()
    return student

def getStudentBy_email(email):
    student = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM students WHERE email = %s', [email])
    if result > 0:
        data = cur.fetchone()   # Fetches the first one "should be just one"
        student = Student(data['id'], data['NIA'], data['name'], data['last_name'],
                          data['last_name_second'], data['email'], data['password'])
    else:
        raise RuntimeError('No student with email: ' + str(email))
        pass

    cur.close()
    return student

def getProfessorBy_email(email):
    student = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM professors WHERE email = %s', [email])
    if result > 0:
        data = cur.fetchone()  # Fetches the first one "should be just one"
        student = Professor(data['id'], data['name'], data['last_name'],
                            data['last_name_second'], data['email'], data['password'])
    else:
        raise RuntimeError('No student with email: ' + str(email))
        pass

    cur.close()
    return student

def getAssigment(id):
    assigment = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM assigments WHERE id = %s', [id])
    if result > 0:
        data = cur.fetchone()  # Fetches the first one "should be just one"

        ### Create assigment object ###
        sections = getSections(data['id'])                                          # First we need to fetch the sections
        assigment = Assigment(sections, data['course'], data['name'], id)           # Second create the assigment object
    else:
        raise RuntimeError('No assigment with id: ' + str(id))
        pass

    cur.close()
    return assigment

def getSections(assigment_id):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM sections WHERE id_assigment = %s', [assigment_id])

    sections = []

    if result > 0:
        # Using the cursor as iterator
        for row in cur:
            tmpSection = Section(row['id'], row['name'], row['order_in_assigment'], row['text'],)
            # assigments[row['id']] = row['name']
            sections.append(tmpSection)

    cur.close()
    return sections

def getSection(id):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM sections WHERE id = %s', [id])
    row = cur.fetchone()
    tmpSection = Section(row['id'], row['name'], row['order_in_assigment'], row['text'], )
    cur.close()
    return tmpSection

def putSection(id_assigment, order_in_assigment, name, text):
    # Execute query
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO sections(id_assigment, order_in_assigment, name, text) VALUES(%s, %s, %s, %s)",
        (id_assigment, order_in_assigment, name, text))
    mysql.connection.commit()               # Commit to DB
    id = cur.lastrowid

    cur.close()
    return id

def putAssigment(course, name, id_professor):
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute(
        "INSERT INTO assigments(name, course, id_professor) VALUES(%s, %s, %s)",
        (name, course, id_professor))
    mysql.connection.commit()               # Commit to DB
    id = cur.lastrowid

    cur.close()                             # Close connection
    return id

def putDoubt(doubt : Doubt, studentGroup : StudentGroup):
    cur = mysql.connection.cursor()

    # 1. Add to doubt table and fill the gaps in doubt obj
    cur.execute(
        "INSERT INTO doubts(text, section) VALUES(%s, %s)",
        (doubt.doubtText, doubt._section.db_id))
    mysql.connection.commit()               # Commit to DB
    doubt.db_id = cur.lastrowid
    fulfillDoubtInfo(doubt)

    # 2. Add doubt to doubt_student table with the students in the group (each of them posted the doubt)
    for student in studentGroup.students:
        cur.execute(
            "INSERT INTO doubt_student(doubt, student) VALUES(%s, %s)",
            (doubt.db_id, student.db_id))
        mysql.connection.commit()           # Commit to DB

    cur.close()                             # Close connection

def getDoubt(id):
    tmpDoubt = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM doubts WHERE id = %s', [id])
    if result > 0:
        data = cur.fetchone()               # Fetches the first one "should be just one"
        ### Complete doubt object ###
        tmpSection = getSection(data['section'])
        tmpDoubt = Doubt(data['text'], tmpSection, data['time'])
    else:
        raise RuntimeError('No doubt with id: ' + str(id))
        pass

    cur.close()
    return tmpDoubt

def fulfillDoubtInfo(doubt : Doubt):
    id = doubt.db_id
    tempDoubt = getDoubt(id)
    doubt._postTime = tempDoubt._postTime

def answerDoubt(doubt : Doubt, text : str, resolver):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO answers(doubt, text) VALUES(%s, %s)",
        (doubt.db_id, text))
    mysql.connection.commit()               # Commit to DB
    cur.close()                             # Close connection
    putAnswerResolver(resolver, cur.lastrowid)
    return cur.lastrowid

def putAnswerResolver(resolver, answer_id):
    cur = mysql.connection.cursor()
    if isinstance(resolver, Professor):
        cur.execute(
            "INSERT INTO answer_resolvers(answer, professor) VALUES(%s, %s)",
            (answer_id, resolver.db_id))
    elif isinstance(resolver, Student):
        cur.execute(
            "INSERT INTO answer_resolvers(answer, student) VALUES(%s, %s)",
            (answer_id, resolver.db_id))

    mysql.connection.commit()               # Commit to DB
    cur.close()                             # Close connection
    return cur.lastrowid