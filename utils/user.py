from mongoengine import *

connect('EPQProject')

class User(Document):
    uuid = StringField()

    username = StringField()
    password = StringField()

    first_name = StringField()
    last_name = StringField()

    is_teacher = BooleanField()

    classes = ListField(StringField())
    homeworks = DictField()

def get_user(uuid):
    user = User.objects.get(uuid=uuid)

    userDict = {}
    for item in user:
        if item == 'id': continue
        userDict[item] = user[item]
    
    return userDict