## Decisiones de diseño:
TypeScript
- El proyecto es grande, los errores en JS son muy comunes y se solucionan fácilmente con TS.
- Fácilmente mantenible
- Fácilmente escalable
- TIENE CLASES (wiiiiiii!)

Vue.js?

## Data structures (Objs)
### Classroom
- Map (x,y) // Rows and columns, assuming evenly distributed classes.
- Stations[] : Station
- Doubts [] : Doubt

### Station
- Group
- Progress // Group.AssigmnentProgress
- Doubt : bool
- PositionInClass (x,y)

### Group
- Students[] : Student
- ProfessorTime
- Assignment : Assignment
- AssigmentProgress
- Doubts[] : Doubt

### Student
- Name
- LastName
- SecondLastName?
- NIA
- Picture

### Doubt
- DoubtText
- Section : Assignment.Section
- Answer? : string
- Answered : bool
- UnanswerdTime // When answered, statistic purposes
- PostTime

### Assignment
- Sections[] : Section

### Section
- AssignmentOrder
- Name
- Text // MD, HTML...?

// The doubts are shared between Classroom and Group, to be easily accessible for both.
