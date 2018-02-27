## Decisiones de diseño:
TypeScript
- El proyecto es grande, los errores en JS son muy comunes y se solucionan fácilmente con TS.
- Fácilmente mantenible
- Fácilmente escalable
- TIENE CLASES (wiiiiiii!)

Vue.js?

## Data structures (Objs)
### [ ] Classroom
- Map (x,y) // Rows and columns, assuming evenly distributed classes.
- Stations[] : Station
- Doubts [] : Doubt

### [x] WorkStation
extends WorkGroup
- Doubt : bool
- PositionInClass (x,y)

### [x] StudentGroup
- Students[] : Student
- ProfessorTime
- Assignment : Assignment
- AssigmentProgress
- Doubts[] : Doubt
- classroom : Classroom // Needed to put doubts there too

### [x] Student
- Name
- LastName
- SecondLastName?
- NIA
- Picture

### [x] Doubt
- DoubtText
- Section : Assignment.Section
- Answer? : string
- Answered : bool
- UnanswerdTime // When answered, statistic purposes
- PostTime

### [x] Assignment
- Sections[] : Section
- Course : Course

### [x] Course
- Degree
- CourseName
- Year

### [x] Section
- AssignmentOrder
- Name
- Text // MD, HTML...?

// The doubts are shared between Classroom and Group, to be easily accessible for both.
