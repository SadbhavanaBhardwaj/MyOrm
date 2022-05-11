import orm_db
from custom_orm.models import Author

mydb = orm_db.get_connection_cursor("my_db")
print(type)

Author.create_table(mydb)

author = Author(name="ishoo", age=34, email="ishoo@gmail.com")
print("author::::::::::", author)
#print(author.__dict__)
author.save()

# author = Author.filter(name="sadbhavana")
# #assert author[0] == ('sadbhavana', 25, datetime.datetime(2022, 5, 8, 23, 35, 16, 411355))
# auth = author
# print(auth.df)
# author.obj_filter(name="sadbhavana",age=35)