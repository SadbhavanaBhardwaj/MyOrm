import email
from traceback import print_tb
from rest_framework.views import APIView
from rest_framework.response import Response

from custom_orm.models import Author


from custom_orm.helper import orm, orm_db
# Create your views here.

class CreateNewOrm(APIView):
    def get(self, request):
        

        mydb = orm_db.get_connection_cursor("my_db")

        Author.create_table(mydb)
        author = Author(name="sadbhavana", age=25, email="ishoo@gmail.com")
        print(type(author))
        print("author::::::::::", author)
        

        author = Author.filter(name="sadbhavana")
        a = author()
        s = a.obj_filter(email="sadbhavana@gmail.com")
        a = s.objs[0]
        a.attributes['email'] = orm.EmailField("sharda@gmail.com")
        
        a.save()
        
        
        
        return Response("doing well")