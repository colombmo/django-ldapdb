from django.db import models
from django.contrib.auth.models import User

'''
#   Models for user management
'''
# Set user email as unique, to avoid email duplicates
User._meta.get_field('email')._unique = True

# Invitation sent to someone, with a secret code and an expiration date
class Invitation(models.Model):
    code = models.CharField(max_length = 30)
    date_created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    sent_to = models.EmailField()
    sent_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
