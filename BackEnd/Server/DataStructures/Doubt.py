from DataStructures import Section
import time
import datetime

class Doubt:
    'Defines a group\'s doubt'
    doubtText = ''
    answerText = ''
    section : Section
    # Protected attributes
    _answered = False
    _postTime : time
    _unanswerdTime = -1             # When answered, statistic purposes

    def __init__(self, doubtText, section : Section):
        self.doubtText = doubtText
        self._section = section
        self._postTime = time.time()

    def set_Answer(self, answerText):
        self._answerText = answerText
        self._answered = True

        # If the professor didn't finish the time we do it
        if (self._unanswerdTime < 0):
            self._unanswerdTime = self._set_UnanseredTime()

    def _set_UnanseredTime(self):
        'Calculates the difference between port time and now'
        self._unanswerdTime = time.time() - self._postTime