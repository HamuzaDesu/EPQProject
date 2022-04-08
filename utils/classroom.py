from mongoengine import *

connect('EPQProject')

class Classroom(Document):
    teacher = UUIDField(binary=False)
    class_code = StringField()
    name = StringField()

    students = ListField(StringField())
    homeworks = ListField(DictField())

def get_class(class_code):
    classroom = Classroom.objects.get(class_code=class_code)

    classDict = {}
    for item in classroom:
        if item == 'id': continue
        classDict[item] = classroom[item]
    
    return classDict
