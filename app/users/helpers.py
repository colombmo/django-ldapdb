'''
# Helper functions
'''
import random
import string
from datetime import datetime, timedelta
from django.contrib import messages
from .models import Invitation


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