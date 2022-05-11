from rest_framework.views import APIView
from rest_framework.response import Response

from custom_orm.helper import orm
# Create your views here.

class CreateInstanceAPIView(APIView):
    def get(self, request):
        conn = orm.create_db("sadbhavana")
        data = {"sad": "bhardwaj"}
        return Response(data)