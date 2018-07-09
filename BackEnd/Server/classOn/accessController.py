from classOn import DBUtils
from passlib.hash import sha256_crypt
from classOn import sessionUtils

class access():

    @staticmethod
    def loginStudent(request, session):
        email = request.form['email']
        password_candidate = request.form['password']
        student = DBUtils.getStudentBy_email(email)  # Load student information from DB if exists (None if not)

        passwordIncorrect = False

        if student is not None:                     # Professor found
            if (sha256_crypt.verify(password_candidate, student.passwordHash)):         # Correct password
                # Session variables
                # Store information while the user is logged in
                # if not sessionUtils.get_isLoggedIn(session):
                if "logged_in" in session:
                    # If is a group add the new member
                    sessionUtils.set_student_id(session,student.db_id)
                else:
                    # If is not a group add just one member
                    sessionUtils.studentLogIn(session, student)
            else:
                passwordIncorrect = True

        return passwordIncorrect

    @staticmethod
    def loginProfessor(request, session):
        # Logging in as professor
        email = request.form['email']
        password_candidate = request.form['password']
        professor = DBUtils.getProfessorBy_email(email)  # Load professor information from DB if exists (None if not)

        passwordIncorrect = False


        if  professor is not None:
            if (sha256_crypt.verify(password_candidate, professor.passwordHash)):         # Correct password
                # Session variables
                # Store information while the user is logged in
                sessionUtils.professorLogIn(session, professor)

            else:
                passwordIncorrect = True

        return passwordIncorrect
