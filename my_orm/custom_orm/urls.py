from django.urls import path
from custom_orm.views import CreateInstanceAPIView

urlpatterns = [
    path('dekho/',  CreateInstanceAPIView.as_view()),
]
