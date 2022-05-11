from rest_framework.views import APIView
from rest_framework.response import Response

from custom_orm.models import Author


from custom_orm.helper import orm, orm_db
# Create your views here.

class CreateNewOrm(APIView):
    def get(self, request):
        

        mydb = orm_db.get_connection_cursor("my_db")
        print(type)

        Author.create_table(mydb)

        author = Author(name="sadbhavana", age=25, email="sadbhavana@gmail.com")
        print("author::::::::::", author)
        #print(author.__dict__)
        #author.save()

        author = Author.filter(name="sadbhavana")
        # #assert author[0] == ('sadbhavana', 25, datetime.datetime(2022, 5, 8, 23, 35, 16, 411355))
        a = next(author())
        print(a.df)
        # auth = author
        # print(auth.df)
        print(a.obj_filter(name="sadbhavana",age=34))
        return Response("doing well")