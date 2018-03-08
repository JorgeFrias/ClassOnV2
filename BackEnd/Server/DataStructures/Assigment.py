### Assignment
from DataStructures import Section
from DataStructures import Course
from typing import List

class Assigment:
    'Defines an assigment'

    # def __init__(self, sections : List[sections], course : course):
    #     self.sections = sections
    #     self.course = course

    def __init__(self, sections, course):
        self.sections = sections            # : List[Sections]
        self.course = course                # : String