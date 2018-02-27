from DataStructures import WorkStation
from  DataStructures import Doubt
from typing import List


class Classroom:
    classSize = (0,0)        # (X,Y) size
    workStations : [WorkStation]
    doubts : List[Doubt] = []

    def __init__(self, classSize : (int,int)):
        self.classSize = classSize
        self.workStations = []
        self.doubts = []
