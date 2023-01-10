from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Invitation
from .forms import InviteForm, NewUserForm

import random
import string
from datetime import datetime, timedelta

from django.http import HttpResponse

 
# Test view
def index(request):
  return HttpResponse("Hello Geeks")


# Dashboard for user management
def dashboard(request):
  return render(request, "users/dashboard.html")

@login_required
def invite(request):
  if request.method == "POST":
    form = InviteForm(request.POST, request)
    if form.is_valid():
      sent_to = form.cleaned_data.get("email_address")
      code = get_random_string(30)
      
      # Create entry in database to remember the sent invitation
      inv, created = Invitation.objects.get_or_create(sent_to = sent_to, 
        defaults={
          "sent_by" : request.user,
          "code" : code})

      if not created:
        inv.sent_by = request.user
        inv.code = code

      inv.save()

      # TODO: Send email with invitation code
      messages.success(request, "Invitation successfully sent." )

      #TODO: Change this. Here we temporarily send the invite code to a template, so that we can try it
      return render(request, "users/invite_sent.html", context={"invite_code" : code})

    messages.error(request, "Unsuccessful registration. Invalid information.")

  form = InviteForm()
  return render(request, "users/invite.html", context={"invite_form" : form})

# Perform a login using django internal system
# TODO: To be changed for LDAP login
def login_request(request):
  if request.user.is_authenticated:
    return redirect("users:dashboard")

  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}.")
        return redirect("users:dashboard")
      else:
        messages.error(request,"Invalid username or password.")
    else:
      messages.error(request,"Invalid username or password.")
  else:
    form = AuthenticationForm()

  return render(request=request, template_name="users/login.html", context={"login_form":form})

# Perform a logout
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("users:dashboard")

# Register user if they have the right invite code
def register_request(request, code = ""):
  if request.user.is_authenticated or len(code) < 10 or not check_invite(request, code):
    return redirect("users:dashboard")

  if request.method == "POST":
    form = NewUserForm(request.POST)
    
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, "Registration successful." )

      # Set invite as already used
      check_invite(request, code, setAsUsed=True)

      return redirect("users:login")
    messages.error(request, "Registration unsuccessful. Correct the following errors:")
  else:
    form = NewUserForm()

  return render(request=request, template_name="users/register.html", context={"register_form": form})

'''
# Helpers
'''

# Get random password of length "length" with letters and digits
def get_random_string(length):
  characters = string.ascii_letters + string.digits
  randstring = ''.join(random.choice(characters) for i in range(length))
  return randstring

# Check if invite code is valid
def check_invite(request, code, setAsUsed = False):
  try:
    invitation = Invitation.objects.get(
      code = code, 
      used = False, 
      date_created__gte = datetime.now() - timedelta(days = 7)
    )

    if setAsUsed:
      invitation.used = True
      invitation.save()

  except Invitation.DoesNotExist:
    messages.error(request, """No valid invite to register with this code.
      Please note that invites are valid only for 7 days.""")
    return False
  
  return True