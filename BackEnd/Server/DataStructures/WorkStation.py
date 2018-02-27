from DataStructures import StudentGroup
from DataStructures import Student
from DataStructures import Assigment

class WorkStation(StudentGroup):
    'In a work station can only be one group'

    unansweredDoubt = False
    positionInClass = (0,0)        # (x, y) position

    def __init__(self, students : [Student], assigment : Assigment, position : (int, int) = (0,0)):
        super.__init__(self, students, assigment)
        self.positionInClass = position