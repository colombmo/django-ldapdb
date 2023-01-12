from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Invitation, LdapGroup, LdapUser
from .forms import InviteForm, NewUserForm, CodeCheckForm
from .helpers import check_invite, get_random_string

from django.http import HttpResponse

 
# Test view
def test(request):
  grp = list(LdapUser.objects.all())
  res = [str(g) for g in grp]
  return HttpResponse("Hello "+str(res))


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

# Perform a login using LDAP
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
  # If empty code, show an interface to manually input it
  if code == "" or not check_invite(request, code):
    form = CodeCheckForm()
    if request.method == "POST":
      form = CodeCheckForm(request.POST)
      if form.is_valid():
        new_code = form.cleaned_data.get('invite_code')
        return redirect("users:register", code = new_code)
    
    return render(request=request, template_name="users/register.html", context={"register_form": form})

  if request.user.is_authenticated:
    return redirect("users:dashboard")

  # Handle the case where a user has sent the form to register themselves on the website
  if request.method == "POST":
    form = NewUserForm(request.POST)
    
    if form.is_valid():
      # Save user in LDAP system
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")
      email = form.cleaned_data.get("email")
      first_name = form.cleaned_data.get("first_name")
      last_name = form.cleaned_data.get("last_name")

      user = LdapUser.objects.create(sn = username, cn = username, uid = username, email = email, first_name = first_name, last_name = last_name, password = password)
      try:
        group = LdapGroup.objects.get(name = "enabled") # Automatically set user as active
        group.members.append(f"cn={username},ou=users,dc=swice,dc=ch")
        group.save()
      except LdapGroup.DoesNotExist:
        pass

      # Save user in django system
      user = form.save()
      user.set_unusable_password() # Save unusable passord in django users system, because we will use LDAP for passwords
      user.save()

      login(request, user)
      messages.success(request, "Registration successful." )

      # Set invite as already used
      check_invite(request, code, setAsUsed=True)

      return redirect("users:dashboard")
    messages.error(request, "Registration unsuccessful. Correct the following errors:")
  else:
    form = NewUserForm()

  return render(request=request, template_name="users/register.html", context={"register_form": form})