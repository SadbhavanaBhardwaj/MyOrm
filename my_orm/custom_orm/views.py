import email
import json
from traceback import print_tb
from rest_framework.views import APIView
from rest_framework.response import Response

from custom_orm.models import Author


from custom_orm.helper import orm, orm_db
# Create your views here.

class CreateNewOrm(APIView):
    def get(self, request):
        
        #create db
        orm.create_db("my_db")
        mydb = orm_db.get_connection_cursor("my_db")

        #create table
        Author.create_table(mydb)

        #object creation
        author = Author(name="ishoo", age=25, email="ishoo@gmail.com")
        
        # saving author in db
        author.save()

        #filtering author on the basis of name -> doesn't hit db rather, it returns an inner function which will filter the data
        author = Author.filter(name="sadbhavana")

        #fetch function(inner func) is called and db is hit and is stored in QuerySet
        #the function returns an object of QuerySet: has list of Author Objects
        a = author()

        #filter the already filtered data
        s = a.obj_filter(email="sharda@gmail.com")

        #updates the object and saves it in db
        if len(s.objs)>0:    
            a = s.objs[0]
            a.attributes['email'] = orm.EmailField("sadbhavana@gmail.com")
            a.save()
        res_data = {}

        #checks if the field name is correct or not
        try:    
            author2 = Author(nam3e="sadbjavam")
        except Exception as e:
            print(e)
            res_data["incorrect_field_name"] = str(e)
    
        return Response(res_data)


class ValidateDataFields(APIView):
    def get(self, req):
            
        res_data = {}
        correct_char_field = orm.CharField("sadbhavana", max_length=40)
        correct_int_field = orm.IntegerField("23")
        correct_email_field = orm.EmailField("sadbhavana.bhardwaj@gmail.com")
        res_data["correct_char_field"] = correct_char_field.value
        res_data["correct_int_field"] = correct_int_field.value
        res_data["correct_email_field"] = correct_email_field.value

        try:    
            incorrect_char_field = orm.CharField("sadbhavana", max_length=4)
        except Exception as e:
            print(e)
            res_data["incorrect_char_field"] = str(e)
        try:    
            incorrect_int_field = orm.IntegerField("s23")
        except Exception as e:
            print(e)
            res_data["incorrect_int_field"] = str(e)
        try:    
            incorrect_email_field = orm.EmailField("sadbhavana.bhardwajgmail.com")
        except Exception as e:
            print(e)
            res_data["incorrect_email_field"] = str(e) + " sadbhavana.bhardwajgmail.com"

        return Response(res_data)

