# Simulation of data structures to check functionality


# ASSIGMENT
from DataStructures import Course, Section, Assigment
course = Course.Course('Computer Science', 'Programing', '2018')
sections = []
sections.append(Section.Section('Chapter one', 1, 'Some text about programning'))
sections.append(Section.Section('Chapter two', 1, 'Some text about something else'))
assigment = Assigment.Assigment(sections, course)

# CLASSROOM
from DataStructures import Classroom
classSize = (5, 10)
classRoom = Classroom.Classroom(classSize)

# STUDENTS & GROUPS
from DataStructures import Student, StudentGroup
student1 = Student.Student('100303030', 'Alice', 'Aliced')
student2 = Student.Student('100303031', 'Bob', 'Bobbed')
student3 = Student.Student('100303032', 'Charly', 'Charlyed')
student4 = Student.Student('100303033', 'Dong', 'Chan')

classRoom.studentGroups.append(StudentGroup.StudentGroup([student1, student2], assigment, classRoom, (0,0)))
classRoom.studentGroups.append(StudentGroup.StudentGroup([student3, student4], assigment, classRoom, (0,1)))

print('Loaded information')