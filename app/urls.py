from django.urls import path
from .views import *

urlpatterns = [
    path('getdata', getdata, name="getdata"),
    path('', Main.as_view(), name="main")
]