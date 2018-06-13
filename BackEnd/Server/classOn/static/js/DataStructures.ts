/**
 * This is a subset of the information of the same classes on the server side.
 * Cause not all the information is needed in the client side.
 */
module DataStructures
{
    export class Student
    {
        db_id: number;
        NIA: string;
        name: string;
        lastName: string;
        email: string;
        secondLastName: string;

        constructor(db_id: number, NIA: string, name: string, lastName: string)
        {
            this.db_id = db_id;
            this.NIA = NIA;
            this.name = name;
            this.lastName = lastName;
        }
    }

    export class StudentGroup
    {
        public students: Student[];
        public position: [number, number];
        public assigmentProgress: number;
        public professorTime: number;
        public doubts: Doubt[];
        public unansweredDoubt: boolean;
        public groupID: number;
        //public doubtsSolved: Doubt[];

        constructor(students: Student[], position: [number, number], assigmentProgress: number, professorTime: number, doubts: Doubt[], groupID: number)
        {
            this.students = students;
            this.position = position;
            this.assigmentProgress = assigmentProgress
            this.professorTime = professorTime;
            this.doubts = doubts;
            this.groupID = groupID;
            if (doubts.length > 0)
                this.unansweredDoubt = false;
            else
                this.unansweredDoubt = true;
        }
    }

    export class Doubt
    {
        public db_id: number;
        public doubtText: string;
        public section: number;
        public postTime: number;
        public studentGroup: StudentGroup;
        public answers: string[];
        public professorSolved: boolean;

        constructor(db_id: number, doubtText: string, section: number, postTime: number, studentGroup: StudentGroup, answers: string[], professorSolved: boolean)
        {
            this.db_id = db_id;
            this.doubtText = doubtText;
            this.section = section;
            this.postTime = postTime;
            this.studentGroup = studentGroup;
            this.answers = answers;
            this.professorSolved = professorSolved;
        }
    }

    export class Answer
    {
        public db_id: number;
        public text: string;

        constructor(db_id: number, text: string)
        {
            this.db_id = db_id;
            this.text = text;
        }
    }
}
    export { DataStructures };
