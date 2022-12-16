from django.contrib import admin
from .models import Location, DataType, Experiment, Group
from .models import Participant, SurveyProperties, PeriodicSurveyProperties
from .models import OnDemandSurveyProperties, OnModeChangeSurveyProperties

from .models import LimeSurvey, LimeSurveyLanguagesettings, LimeQuestion
from .models import LimeQuestionL10N, LimeGroup, LimeGroupL10N

# Register your models here.
admin.site.register(Location)
admin.site.register(DataType)
admin.site.register(Experiment)
admin.site.register(Group)
admin.site.register(Participant)
admin.site.register(SurveyProperties)
admin.site.register(PeriodicSurveyProperties)
admin.site.register(OnDemandSurveyProperties)
admin.site.register(OnModeChangeSurveyProperties)
admin.site.register(LimeSurvey)
admin.site.register(LimeSurveyLanguagesettings)
admin.site.register(LimeQuestion)
admin.site.register(LimeQuestionL10N)
admin.site.register(LimeGroup)
admin.site.register(LimeGroupL10N)