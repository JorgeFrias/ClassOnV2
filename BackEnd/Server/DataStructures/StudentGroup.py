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
    doubts : List[Doubt] = []
    _classroom : Classroom

    def __init__(self, students : [Student], assigment : Assigment, classRoom : Classroom):
        self.students = students
        self.assigment = assigment
        self._classroom = classRoom
        # self.doubts = classRoom.doubts          # Reference to class doubts

    def addDoubt(self, doubt : Doubt):
        'Adds doubt to groups doubt and to classroom doubts'
        self.doubts.append(doubt)
        self._classroom.doubts.append(doubt)

