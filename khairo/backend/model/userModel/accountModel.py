from uuid import uuid4
from datetime import datetime
from mongoengine import *




class UserAccount(Document):
    firstname = StringField(required=True, min_length=3)
    lastname = StringField(required=True, min_length=3)
    email = EmailField(required=True,  unique=True)
    password = StringField(required=True)
    active   = BooleanField(default=False)
    admin    = BooleanField(default=False)
    created_at = DateField(default=datetime.utcnow)
    meta  = {"db_alias":"core", "collection":"user"}

    @queryset_manager
    def get_singleUserByEmail(doc_cls, queryset, email):
        return queryset.filter(email=email).first()

    @queryset_manager
    def get_singleUserById(doc_cls, queryset, userId):
        return queryset.filter(id=userId).first()


    def to_json(self, *args, **kwargs):
        return {
            "id":str(self.pk),
            "firstname":self.firstname,
            "lastname":self.lastname,
            "email":self.email,
            "active":self.active,
            "created_at":str(self.created_at)
        }











