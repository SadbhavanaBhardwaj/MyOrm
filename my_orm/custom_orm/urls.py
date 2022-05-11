from django.urls import path
from custom_orm.views import CreateNewOrm

urlpatterns = [
    path('dekho/',  CreateNewOrm.as_view()),
]
