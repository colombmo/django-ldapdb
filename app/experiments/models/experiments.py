from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from .limesurvey import *

'''
#   Objects
'''

# Locations where the experiments will be executed. For example: SLL, Suurstoffi
class Location(models.Model):
    name = models.CharField(max_length = 255, help_text = "For example \"Smart Living Lab\"")
    city = models.CharField(max_length = 255, help_text = "For example \"Fribourg\"")


# Types of data to be collected for an experiment (e.g., by the app or building data)
class DataType(models.Model):
    name = models.CharField(max_length = 255, help_text = "Extended name of the type of data to be collected (e.g., Mobility data)")
    variable_name = models.CharField(max_length = 255, help_text = "Name of the variable showing what type of data is used (e.g., mobility_data)")


# Experiments with their basic settings
class Experiment(models.Model):
    name = models.CharField(max_length = 255, help_text = "Title of the experiment")
    description = models.TextField(help_text = "Description of the experiment")
    publish = models.BooleanField(help_text = "Select this to make this experiment available to everyone, otherwise it will be accessible only in test mode")
    created_by = User()
    
    ## TODO: Start and end date??

    ## Many to many relationships
    location = models.ManyToManyField(Location, help_text = "The locations where this experiment is taking place")


# Group to be created inside the experiment, to do between-group experiments
class Group(models.Model):
    parent_experiment = models.ForeignKey(Experiment, on_delete = models.CASCADE, help_text = "The experiment to which this group belongs")
    name = models.CharField(max_length = 255, help_text = "Name of the group")
    conditions_to_belong = models.CharField(max_length = 255, help_text = "Summarization of the conditions to be included in this group (e.g., age > 40")


# Data to be collected, with a description of the reason for such a collection
class CollectedData(models.Model):
    data_type = models.ForeignKey(DataType, on_delete = models.CASCADE, help_text = "The type of data to be collected")
    experiment = models.ForeignKey(Experiment, on_delete = models.CASCADE, help_text = "The experiment for which to collect this data")
    description = models.TextField(help_text = "Description of the reason for which collecting this data is important")


# User object containing the unique personal code
class Participant(models.Model):
    user_key = models.CharField(max_length = 20, help_text = "The unique user identifier, generated with persnal information")

    # Many to many relationships
    experiment = models.ManyToManyField(Experiment, help_text = "The list of experiments where this participant is enrolled")
    group = models.ManyToManyField(Group, help_text = "The groups to which this participant belongs")


# Properties to handle surveys
class SurveyProperties(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete = models.CASCADE, 
        help_text = "The experiment where this survey will be executed")
    survey = LimeSurvey()

    # Many to many relationships
    target_groups = models.ManyToManyField(Group)

# Periodic survey
class PeriodicSurveyProperties(models.Model):
    start_on = models.DateTimeField(help_text = "Date when to start sending out surveys")
    end_on = models.DateTimeField(help_text = "Date when to stop sending out surveys")
    repeats = models.CharField(max_length = 15,
        choices = [("daily", "daily"), 
                    ("weekly", "weekly"), 
                    ("monthly", "monthly")], 
        help_text = "How often this survey is repeated")
    every = models.SmallIntegerField()
    on_day = models.SmallIntegerField()
    reminder = models.BooleanField(default = False, help_text = "If people do not answer, send a reminder after 3 days")

    parent_survey = models.OneToOneField(SurveyProperties, on_delete = models.CASCADE)

# On-demand survey
class OnDemandSurveyProperties(models.Model):
    reminder = models.BooleanField(default = False, help_text = "If people do not answer, send a reminder after 3 days")

    parent_survey = models.OneToOneField(SurveyProperties, on_delete = models.CASCADE)

# On event "transportation mode changed" survey
class OnModeChangeSurveyProperties(models.Model):
    from_event = models.CharField(max_length = 20, 
        choices = [("STILL", "still"), 
                    ("WALKING", "walking"), 
                    ("RUNNING", "running"),
                    ("CYCLING", "cycling"), 
                    ("TRAIN", "train"), 
                    ("CAR", "car"), 
                    ("BUS", "bus"), 
                    ("TRAM", "tram"), 
                    ("ANY", "any")],
        help_text = "The activity before the mode of transport change")

    to_event = models.CharField(max_length = 20,
        choices = [("STILL", "still"), 
                    ("WALKING", "walking"), 
                    ("RUNNING", "running"),
                    ("CYCLING", "cycling"), 
                    ("TRAIN", "train"), 
                    ("CAR", "car"), 
                    ("BUS", "bus"), 
                    ("TRAM", "tram"), 
                    ("ANY", "any")],
        help_text = "The activity to which the mode of transport changed")

    parent_survey = models.OneToOneField(SurveyProperties, on_delete = models.CASCADE)