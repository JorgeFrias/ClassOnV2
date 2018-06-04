from typing import Mapping, Sequence
import time
from PIL import Image
import uuid

class Student:
    'Represents a student'
    def __init__(self, db_id, nia, name, lastName, seccondLastName = '', email = '', passwordHash = '', pictureSrc = ''):
        self.db_id = db_id
        self.NIA = nia
        self.name = name
        self.lastName = lastName
        self.email = email
        self.passwordHash = passwordHash
        self.secondLastName = seccondLastName


        if (pictureSrc is not ''):
            try:
                self.picture = Image.open(pictureSrc)
            except:
                raise Exception('error opening picture: ' + pictureSrc)

    def __dict__(self):
        result = {}
        result['db_id'] = self.db_id
        result['name'] = self.name
        result['lastName']  = self.lastName

        return result

    def JSON(self):
        result = '{\n'
        result += '\"db_id\":\"' + str(self.db_id) + '\", \n'
        result += '\"name\":\"' + str(self.name) + '\", \n'
        result += '\"lastName\":\"' + str(self.lastName) + '\" \n'
        result += '}'
        return result

class Course:
    'Defines a course'
    def __init__(self, degree = 'na', courseName = 'na', year = 'na'):
        self.degree = degree
        self.name = courseName
        self.year = year

class Section:
    'Defines a section of an Assigment'
    def __init__(self, db_id, name, orderInAssigment, sectionText):
        self.name = name
        if (orderInAssigment > 0):
            self.order = orderInAssigment
        else:
            raise ValueError('orderInAssigment must be bigger than zero')
        self.text = sectionText
        self.db_id = db_id

class Assigment:
    'Defines an assigment'
    def __init__(self, sections : Sequence[Section], course : Course = None, name : str = '', db_id = 0):
        self.name = name
        self.sections = sections            # : List[Sections]
        self.course = course                # : String
        self.db_id = db_id

    def sections_dict(self):
        result = []
        for section in self.sections:
            result.append(vars(section))
        return result

class Professor():
    def __init__(self, db_id, name, lastName, lastNameSecond, email, passwordHash = ''):
        self.db_id = db_id
        self.name = name
        self.lastName = lastName
        self.lastNameSecond = lastNameSecond
        self.email = email
        self.passwordHash = passwordHash

class StudentGroup:
    def __init__(self, students : [Student], position : (int, int) = (0, 0)):
        self.students = students
        self.positionInClass = position
        self.assigmentProgress = 0
        self.professorTime = 0
        self.doubts = []
        self.doubtsSolved = []
        self.unansweredDoubt = False
        self.groupID = str(uuid.uuid4())        # Generates an ID

    def JSON(self):
        result = '{\n'
        result += '\"position\":\"' + str(self.positionInClass[0]) + '_' + str(self.positionInClass[1]) + '\", \n'
        result += '\"id\":\"' + str(self.groupID) + '\", \n'
        result += '\"assigmentProgress\":\"' + str(self.assigmentProgress) + '\", \n'
        result += '\"students\": [ \n'
        for student in self.students:
            result += student.JSON() + ','
        result = result[:-1]                    # Remove last comma
        result += ' ] \n'
        result += '}'

        return result

    def positionInClass_str(self):
        return str(self.positionInClass[0]) + '_' + str(self.positionInClass[1])

    def addStudent(self, student : Student):
        '''
        Adds an student to the given group if is not in the group
        :param student: Student to add
        :return: void
        '''
        # any(x.name == "t2" for x in l)
        if (not any(studentInGroup.db_id == student.db_id for studentInGroup in self.students)):
            # Is not in the group
            self.students.append(student)

    def solveDoubt(self, doubtID : int):
        self.doubts.remove(id)
        self.doubtsSolved.append(id)
        if (len(self.doubts) < 1):
            # No doubts
            self.unansweredDoubt = False

class Doubt:

    'Defines a group\'s doubt'
    def __init__(self, doubtText, section : Section, studentGroup : StudentGroup, postToDB = True):
        self.db_id = -1
        self.doubtText = doubtText
        self._section = section
        self._postTime = 0
        self._studentGroup = studentGroup
        self.postTime = 0
        self.answers = []

    def JSON(self):
        result = '{\n'
        result += '\"db_id\":\"' + str(self.db_id) + '\", \n'
        result += '\"text\":\"' + self.doubtText.strip().replace('\n', '\\n').replace('\r', '') + '\", \n'
        result += '\"section\":\"' + str(self._section.order) + '\", \n'
        result += '\"postTime\":\"' + str(self._postTime) + '\", \n'
        result += '\"group\":\"' + self._studentGroup.positionInClass_str() + '\", \n'
        # Add all answers
        result += '\"answers\": [ \n'
        for answ in self.answers:
            result += answ.JSON() + ',\n'
        if len(self.answers) > 0:
            result = result[:-2]                    # Remove last comma
        result += ']  \n'                           # Close list
        result += '}'
        return result

    def postToDB(self):
        from classOn import DBUtils
        DBUtils.putDoubt(self, self._studentGroup)

    def add_Answer(self, answerText, resolver, postToDB = True):
        from classOn import DBUtils
        self._answerText = answerText
        db_id = -1
        if postToDB:
            db_id = DBUtils.answerDoubt(self, answerText, resolver)
        answ = DoubtAnswer(db_id, answerText)
        self.answers.append(answ)

    def _set_UnanseredTime(self):
        'Calculates the difference between post time and now'
        self._unanswerdTime = time.time() - self._postTime

class DoubtAnswer:
    def __init__(self, db_id = -1, text = ''):
        self.db_id = db_id
        self.text = text

    def JSON(self):
        result = '{\n'
        result += '\"db_id\":\"' + str(self.db_id) + '\", \n'
        result += '\"text\":\"' + str(self.text) + '\" \n'
        result += '}'
        return result


class Classroom:

    def __init__(self, classSize: (int, int), professor: Professor, assigment: Assigment, room=''):
        self.id = str(uuid.uuid4())
        self.classSize = classSize
        self.professor = professor
        self.assigment = assigment
        self.studentGroups = dict()  # Groups in class
        self.doubts = []
        self.doubtsSolved = []
        self.__doubtsIdCounter = 0
        self.room = room

    def addDoubt(self, doubt: Doubt):
        tupleDoubt = (doubt.db_id, doubt)
        self.doubts.append(tupleDoubt)

    def getDoubt(self, doubt_id):
        doubt = [doubt for doubt in self.doubts if doubt[0] == doubt_id]
        return doubt[0][1]             # Should be just once

    def addStudentToPlace(self, student: Student, place: (int, int)):
        '''
        Adds an student to a given place in the classroom, if there is a group already assign the student to the
        group, if not crates the group.
        :param student:
        :param place:
        :return: The group object the student belongs to.
        '''
        added = False
        for group_id, group in self.studentGroups.items():  # Check if is a group for the desired place
            tmpPlace = group.positionInClass
            if tmpPlace == place:
                added = True
                # group.students.append(student)            # Add student to
                group.addStudent(student)
                return group

        if added == False:  # There is no group, create with one student
            tmpGroup = StudentGroup([student], place)
            self.studentGroups[tmpGroup.groupID] = tmpGroup  # Add group to global object
            return tmpGroup

    def filledPlaces(self):
        rows = self.classSize[0]
        cols = self.classSize[1]
        result = []
        for id, group in self.studentGroups.items():
            result.append(group.positionInClass)
        return result

    def filledPlacesStrList(self):
        rows = self.classSize[0]
        cols = self.classSize[1]
        result = []
        for id, group in self.studentGroups.items():
            result.append(str(group.positionInClass[0]) + '_' + str(group.positionInClass[1]))
        return result

    def filledPlacesJSON(self):
        result = '{ \n'
        filledPlacesList = self.filledPlaces()
        for place in filledPlacesList:
            result += str(place[0]) + '_' + str(place[1]) + ',\n'
        result = result[:-2]  # Remove ',\n'
        result += '\n}'
        return result
