class Course:
    'Defines a course'
    degree = ''
    courseName = ''
    year = ''

    def __init__(self, degree, courseName, year):
        self.degree = degree
        self.courseName = courseName
        self.year = year
