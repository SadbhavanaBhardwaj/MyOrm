import datetime  
from custom_orm.helper import orm_db, orm
# from django.db import models

from django.db import models

# Create your models here.

class Author(orm.Model):
    table_name = "author"
    name = orm.CharField(max_length=87)
    age = orm.IntegerField()
    email = orm.EmailField()

