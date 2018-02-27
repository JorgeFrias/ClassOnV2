class Section:
    'Defines a section of an Assigment'
    name = ''
    assigmentOrder = 0
    text = ''

    def __init__(self, name, orderInAssigment, sectionText):
        self.name = name
        if (orderInAssigment > 0):
            self.assigmentOrder = orderInAssigment
        else:
            raise ValueError('orderInAssigment must be bigger than zero')
        self.text = sectionText