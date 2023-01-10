from django.urls import path
#now import the views.py file into this code
from . import views

app_name = "users"

urlpatterns=[
    path('',views.index),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('invite/', views.invite, name="invite"),
    path('login/', views.login_request, name="login"),
]