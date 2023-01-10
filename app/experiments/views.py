from django.shortcuts import render
from django.http import HttpResponse
 
 
# Test view
def index(request):
  return HttpResponse("Hello Geeks")
