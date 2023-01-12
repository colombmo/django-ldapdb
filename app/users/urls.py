from django.urls import path
#now import the views.py file into this code
from . import views

app_name = "users"

urlpatterns=[
    path('',views.dashboard, name="dashboard"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('invite/', views.invite, name="invite"),
    path('login/', views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("register/<code>", views.register_request, name="register"),
    path("register/", views.register_request, name="register"),
    path('test/', views.test, name="test"),
]