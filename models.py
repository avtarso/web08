from mongoengine import Document
from mongoengine.fields import ReferenceField, DateField, ListField, StringField


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)