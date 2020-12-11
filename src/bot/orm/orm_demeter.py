from mongoengine import *

class Melisa(Document):
    name = StringField(max_length=50)
    url_post = URLField(required=True)
    token = StringField(max_length=10)    

class User(Document):
    melisa = ReferenceField(Melisa)
    user_id = StringField(required=True)

class Slot(EmbeddedDocument):
    name = StringField()
    values = ListField(StringField())

class Chat(Document):
    user = ReferenceField(User)
    text = StringField(required=True)
    date = DateTimeField(required=True)
    intent_id = IntField()
    intent_name = StringField(max_length=30)
    ext_id = StringField(max_length=200)
    slots = DictField()
    