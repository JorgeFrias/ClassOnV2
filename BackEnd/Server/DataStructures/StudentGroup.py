from DataStructures import Student
from DataStructures import Assigment
from DataStructures import Doubt
from DataStructures import Classroom

from typing import List


class StudentGroup:
    '''- Students[] : Student
    - ProfessorTime
    - Assignment : Assignment
    - AssigmentProgress
    - Doubts[] : Doubt'''

    students : List[Student] = []
    assigment : Assigment
    assigmentProgress = 0
    professorTime = 0
    doubts : List[int] = []
    doubtsSolved : List[int] = []
    _classroom : Classroom

    unansweredDoubt = False
    positionInClass = (0,0)        # (x, y) position


    def __init__(self, students : [Student], assigment : Assigment, classRoom : Classroom, position : (int, int) = (0,0)):
        self.students = students
        self.assigment = assigment
        self._classroom = classRoom
        self.positionInClass = position
        # self.doubts = classRoom.doubts          # Reference to class doubts

    def addDoubt(self, doubt : Doubt):
        'Adds doubt to groups doubt'
        self.doubts.append(doubt.id)
        self.unansweredDoubt = True

    def solveDoubt(self, doubtID : int):
        self.doubts.remove(id)
        self.doubtsSolved.append(id)
        if (len(self.doubts) < 1):
            # No doubts
            self.unansweredDoubt = False