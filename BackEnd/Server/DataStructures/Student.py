from PIL import Image

class Student:
    'Represents a student'
    name = ''
    lastName = ''
    secondLastName = ''
    NIA = ''
    picture : Image

    def __init__(self, nia, name, lastName, seccondLastName = '', pictureSrc = ''):
        self.NIA = nia
        self.name = name
        self.lastName = lastName
        self.secondLastName = seccondLastName

        if (pictureSrc is not ''):
            try:
                self.picture = Image.open(pictureSrc)
            except:
                raise Exception('error opening picture: ' + pictureSrc)