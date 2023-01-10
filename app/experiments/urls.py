from django.urls import path
#now import the views.py file into this code
from . import views

app_name = "experiments"

urlpatterns=[
    path('',views.index)
]