from typing import Mapping, Sequence
import time
from PIL import Image

class Student:
    'Represents a student'
    name = ''
    lastName = ''
    secondLastName = ''
    NIA = ''
    picture : Image

    def __init__(self, nia, name, lastName, seccondLastName = '', pictureSrc = ''):
        self.NIA = nia
        self.name = name
        self.lastName = lastName
        self.secondLastName = seccondLastName

        if (pictureSrc is not ''):
            try:
                self.picture = Image.open(pictureSrc)
            except:
                raise Exception('error opening picture: ' + pictureSrc)

class Classroom:
    classSize = (0,0)        # (X,Y) size
    studentGroups = []             # Groups in class
    doubts = []            # Doubt and Group with doubt

    doubtsSolved = []
    __doubtsIdCounter = 0

    def __init__(self, classSize : (int,int)):
        self.classSize = classSize
        # self.workStations = []
        # self.doubts = []

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

class StudentGroup:
    '''- Students[] : Student
    - ProfessorTime
    - Assignment : Assignment
    - AssigmentProgress
    - Doubts[] : Doubt'''

    students = []
    assigment = None
    assigmentProgress = 0
    professorTime = 0
    doubts = []
    doubtsSolved = []
    _classroom  = None

    unansweredDoubt = False
    positionInClass = (0,0)        # (x, y) position


    def __init__(self, students : [Student], assigment : assigment, classRoom : Classroom, position : (int, int) = (0, 0)):
        self.students = students
        self.assigment = assigment
        self._classroom = classRoom
        self.positionInClass = position
        # self.doubts = classRoom.doubts          # Reference to class doubts

    # def addDoubt(self, doubt : Doubt):
    #     'Adds doubt to groups doubt'
    #     self.doubts.append(doubt.id)
    #     self.unansweredDoubt = True

    def solveDoubt(self, doubtID : int):
        self.doubts.remove(id)
        self.doubtsSolved.append(id)
        if (len(self.doubts) < 1):
            # No doubts
            self.unansweredDoubt = False

class Course:
    'Defines a course'
    def __init__(self, degree = 'na', courseName = 'na', year = 'na'):
        self.degree = degree
        self.name = courseName
        self.year = year

class Section:
    'Defines a section of an Assigment'
    name = ''
    order = 0
    text = ''

    def __init__(self, name, orderInAssigment, sectionText):
        self.name = name
        if (orderInAssigment > 0):
            self.order = orderInAssigment
        else:
            raise ValueError('orderInAssigment must be bigger than zero')
        self.text = sectionText

class Assigment:
    'Defines an assigment'

    # def __init__(self, sections : List[sections], course : course):
    #     self.sections = sections
    #     self.course = course

    def __init__(self, sections : Sequence[Section], course : Course):
        self.sections = sections            # : List[Sections]
        self.course = course                # : String

    def sections_dict(self):
        # sectionsDict = {x.assigmentOrder: vars(x) for x in self.sections}
        # return sectionsDict
        result = []
        for section in self.sections:
            result.append(vars(section))

        return result

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




