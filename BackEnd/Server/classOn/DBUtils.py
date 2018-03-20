from dataStructures import Assigment, Section, Professor

''' MySQL import '''
from classOn import mysql

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

def getAssigment(id):
    assigment = None
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM assigments WHERE id = %s', [id])
    if result > 0:
        data = cur.fetchone()  # Fetches the first one "should be just one"

        ### Create assigment object ###
        sections = getSections(data['id'])                                      # First we need to fetch the sections
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

def putSection(id_assigment, order_in_assigment, name, text):
    # Execute query
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO sections(id_assigment, order_in_assigment, name, text) VALUES(%s, %s, %s, %s)",
        (id_assigment, order_in_assigment, name, text))
    mysql.connection.commit()  # Commit to DB
    id = cur.lastrowid

    cur.close()
    return id

def putAssigment(course, name, id_professor):
    cur = mysql.connection.cursor()
    # Execute query
    cur.execute(
        "INSERT INTO assigments(name, course, id_professor) VALUES(%s, %s, %s)",
        (name, course, id_professor))
    mysql.connection.commit()  # Commit to DB
    id = cur.lastrowid

    cur.close()  # Close connection
    return id
