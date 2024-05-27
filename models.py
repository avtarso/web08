from mongoengine import Document
from mongoengine.fields import ReferenceField, DateField, ListField, StringField, BooleanField


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    send_sms = BooleanField(required=True, default=False)
    send_email = BooleanField(required=True, default=False)
    born_date = DateField()
