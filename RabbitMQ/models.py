from mongoengine import Document, StringField, BooleanField, connect

connect('contacts_db', host='localhost', port=27017)

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    is_sent = BooleanField(default=False)
    phone_number = StringField()
    address = StringField()
