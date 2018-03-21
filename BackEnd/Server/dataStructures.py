from typing import Mapping, Sequence
import time
from PIL import Image
import uuid


class Student:
    'Represents a student'
    name = ''
    lastName = ''
    secondLastName = ''
    NIA = ''
    picture : Image

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

class Classroom:

    def __init__(self, classSize : (int,int), professor : Professor, assigment : Assigment, room = ''):
        self.classSize = classSize
        self.professor = professor
        self.assigment = assigment
        self.studentGroups = []             # Groups in class
        self.doubts = []
        self.doubtsSolved = []
        self.__doubtsIdCounter = 0
        self.room = room

    def newDoubtID(self) -> int:
        self.__doubtsIdCounter += 1
        return self.__doubtsIdCounter

    def resolDoubt(self, id : int):
        for tupleDoubt in self.doubts:
            if(tupleDoubt[0] == id):
                # Resolve doubt
                tupleDoubt[1].solveDoubt(id)
                self.doubtsSolved.append(tupleDoubt)
                self.doubtsSolved.remove(tupleDoubt)
                break

    def addStudentToPlace(self, student :Student, place : (int, int)):
        '''
        Adds an student to a given place in the classroom, if there is a group already assign the student to the
        group, if not crates the group.
        :param student:
        :param place:
        :return: The group object the student belongs to.
        '''
        added = False
        for group in self.studentGroups:                # Look if is a group for the desired place
            tmpPlace = group.positionInClass
            if tmpPlace == place:
                added = True
                # group.students.append(student)          # Add student to
                group.addStudent(student)
                return group

        if added == False:                              # There is no group, create with one student
            tmpGroup = StudentGroup([student], place)
            self.studentGroups.append(tmpGroup)         # Add group to global object
            return tmpGroup

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
    id = -1
    doubtText = ''
    answerText = ''
    section = None
    # Protected attributes
    _answered = False
    _postTime = None
    _unanswerdTime = -1             # When answered, statistic purposes
    _studentGroup  = None
    _classroom = None

    def __init__(self, doubtText, section : section, studentGroup : StudentGroup, classroom : Classroom):
        self.id = classroom.newDoubtID()
        self._classroom = classroom
        self.doubtText = doubtText
        self._section = section
        self._postTime = time.time()
        self._studentGroup = studentGroup

    def set_Answer(self, answerText):
        self._answerText = answerText
        self._answered = True

        # If the professor didn't finish the time we do it
        if (self._unanswerdTime < 0):
            self._unanswerdTime = self._set_UnanseredTime()

    def _set_UnanseredTime(self):
        'Calculates the difference between port time and now'
        self._unanswerdTime = time.time() - self._postTime

