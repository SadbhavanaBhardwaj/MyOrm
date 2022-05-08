from django.db import models

from custom_orm.helper import orm_db

def create_db(name):
    return orm_db.create_db(name)
    

class Model(models.Model):
    pass