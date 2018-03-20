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

    return sections