from django.urls import path
from custom_orm.views import CreateNewOrm, ValidateDataFields

urlpatterns = [
    path('orm_testing/',  CreateNewOrm.as_view()),
    path("data_types_testing", ValidateDataFields.as_view())
]
