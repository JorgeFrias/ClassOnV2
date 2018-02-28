from DataStructures import StudentGroup
from  DataStructures import Doubt
from typing import List


class Classroom:
    classSize = (0,0)        # (X,Y) size
    studentGroups : [StudentGroup] = []             # Groups in class
    doubts : (Doubt, StudentGroup)  = []            # Doubt and Group with doubt

    doubtsSolved : (Doubt, StudentGroup)  = []
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


