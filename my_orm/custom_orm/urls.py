from django.urls import path
from custom_orm.views import CreateNewOrm

urlpatterns = [
    path('orm_testing/',  CreateNewOrm.as_view()),
]
