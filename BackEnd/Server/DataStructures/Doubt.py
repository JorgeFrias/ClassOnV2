from DataStructures import Section
from DataStructures import Classroom
from DataStructures import StudentGroup

import time
import datetime

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