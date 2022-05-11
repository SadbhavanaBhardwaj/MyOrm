import datetime  
from custom_orm.helper import orm_db, orm
# from django.db import models

from custom_orm.helper import orm

# Create your models here.


class Author(orm.Model):
    table_name = "author"
    name = orm.CharField(max_length=87)
    age = orm.IntegerField()
    email = orm.EmailField()

mydb = orm_db.get_connection_cursor("my_db")
print(type)

Author.create_table(mydb)

author = Author(name="sadbhavana", age=24, email="sadbhavana@gmail.com")
#print(author.__dict__)
author.save()


# author = Author.filter(name="sadbhavana")
# #assert author[0] == ('sadbhavana', 25, datetime.datetime(2022, 5, 8, 23, 35, 16, 411355))
# auth = author
# print(auth.df)
# author.obj_filter(name="sadbhavana",age=35)