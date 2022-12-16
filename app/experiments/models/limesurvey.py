from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

'''
#   Objects
'''

class LimeSurvey(models.Model):
    sid = models.AutoField(primary_key=True)
    owner_id = models.IntegerField()
    gsid = models.IntegerField(blank=True, null=True)
    admin = models.CharField(max_length=50, blank=True, null=True)
    active = models.CharField(max_length=1)
    expires = models.DateTimeField(blank=True, null=True)
    startdate = models.DateTimeField(blank=True, null=True)
    adminemail = models.CharField(max_length=254, blank=True, null=True)
    anonymized = models.CharField(max_length=1)
    format = models.CharField(max_length=1, blank=True, null=True)
    savetimings = models.CharField(max_length=1)
    template = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    additional_languages = models.TextField(blank=True, null=True)
    datestamp = models.CharField(max_length=1)
    usecookie = models.CharField(max_length=1)
    allowregister = models.CharField(max_length=1)
    allowsave = models.CharField(max_length=1)
    autonumber_start = models.IntegerField()
    autoredirect = models.CharField(max_length=1)
    allowprev = models.CharField(max_length=1)
    printanswers = models.CharField(max_length=1)
    ipaddr = models.CharField(max_length=1)
    ipanonymize = models.CharField(max_length=1)
    refurl = models.CharField(max_length=1)
    datecreated = models.DateTimeField(blank=True, null=True)
    showsurveypolicynotice = models.IntegerField(blank=True, null=True)
    publicstatistics = models.CharField(max_length=1)
    publicgraphs = models.CharField(max_length=1)
    listpublic = models.CharField(max_length=1)
    htmlemail = models.CharField(max_length=1)
    sendconfirmation = models.CharField(max_length=1)
    tokenanswerspersistence = models.CharField(max_length=1)
    assessments = models.CharField(max_length=1)
    usecaptcha = models.CharField(max_length=1)
    usetokens = models.CharField(max_length=1)
    bounce_email = models.CharField(max_length=254, blank=True, null=True)
    attributedescriptions = models.TextField(blank=True, null=True)
    emailresponseto = models.TextField(blank=True, null=True)
    emailnotificationto = models.TextField(blank=True, null=True)
    tokenlength = models.IntegerField()
    showxquestions = models.CharField(max_length=1, blank=True, null=True)
    showgroupinfo = models.CharField(max_length=1, blank=True, null=True)
    shownoanswer = models.CharField(max_length=1, blank=True, null=True)
    showqnumcode = models.CharField(max_length=1, blank=True, null=True)
    bouncetime = models.IntegerField(blank=True, null=True)
    bounceprocessing = models.CharField(max_length=1, blank=True, null=True)
    bounceaccounttype = models.CharField(max_length=4, blank=True, null=True)
    bounceaccounthost = models.CharField(max_length=200, blank=True, null=True)
    bounceaccountpass = models.TextField(blank=True, null=True)
    bounceaccountencryption = models.CharField(max_length=3, blank=True, null=True)
    bounceaccountuser = models.CharField(max_length=200, blank=True, null=True)
    showwelcome = models.CharField(max_length=1, blank=True, null=True)
    showprogress = models.CharField(max_length=1, blank=True, null=True)
    questionindex = models.IntegerField()
    navigationdelay = models.IntegerField()
    nokeyboard = models.CharField(max_length=1, blank=True, null=True)
    alloweditaftercompletion = models.CharField(max_length=1, blank=True, null=True)
    googleanalyticsstyle = models.CharField(max_length=1, blank=True, null=True)
    googleanalyticsapikey = models.CharField(max_length=25, blank=True, null=True)
    tokenencryptionoptions = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lime_surveys'


class LimeSurveyLanguagesettings(models.Model):
    id = models.AutoField(primary_key=True)
    surveyls_survey_id = models.ForeignKey(LimeSurvey, db_column = "surveyls_survey_id", on_delete = models.CASCADE)
    surveyls_language = models.CharField(max_length=45)
    surveyls_title = models.CharField(max_length=200)
    surveyls_description = models.TextField(blank=True, null=True)
    surveyls_welcometext = models.TextField(blank=True, null=True)
    surveyls_endtext = models.TextField(blank=True, null=True)
    surveyls_policy_notice = models.TextField(blank=True, null=True)
    surveyls_policy_error = models.TextField(blank=True, null=True)
    surveyls_policy_notice_label = models.CharField(max_length=192, blank=True, null=True)
    surveyls_url = models.TextField(blank=True, null=True)
    surveyls_urldescription = models.CharField(max_length=255, blank=True, null=True)
    surveyls_email_invite_subj = models.CharField(max_length=255, blank=True, null=True)
    surveyls_email_invite = models.TextField(blank=True, null=True)
    surveyls_email_remind_subj = models.CharField(max_length=255, blank=True, null=True)
    surveyls_email_remind = models.TextField(blank=True, null=True)
    surveyls_email_register_subj = models.CharField(max_length=255, blank=True, null=True)
    surveyls_email_register = models.TextField(blank=True, null=True)
    surveyls_email_confirm_subj = models.CharField(max_length=255, blank=True, null=True)
    surveyls_email_confirm = models.TextField(blank=True, null=True)
    surveyls_dateformat = models.IntegerField()
    surveyls_attributecaptions = models.TextField(blank=True, null=True)
    email_admin_notification_subj = models.CharField(max_length=255, blank=True, null=True)
    email_admin_notification = models.TextField(blank=True, null=True)
    email_admin_responses_subj = models.CharField(max_length=255, blank=True, null=True)
    email_admin_responses = models.TextField(blank=True, null=True)
    surveyls_numberformat = models.IntegerField()
    attachments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lime_surveys_languagesettings'
        unique_together = (('surveyls_survey_id', 'surveyls_language'),)


class LimeQuestion(models.Model):
    qid = models.AutoField(primary_key=True)
    parent_qid = models.IntegerField()
    sid = models.IntegerField()
    gid = models.IntegerField()
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=20)
    preg = models.TextField(blank=True, null=True)
    other = models.CharField(max_length=1)
    mandatory = models.CharField(max_length=1, blank=True, null=True)
    encrypted = models.CharField(max_length=1, blank=True, null=True)
    question_order = models.IntegerField()
    scale_id = models.IntegerField()
    same_default = models.IntegerField()
    relevance = models.TextField(blank=True, null=True)
    question_theme_name = models.CharField(max_length=150, blank=True, null=True)
    modulename = models.CharField(max_length=255, blank=True, null=True)
    same_script = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lime_questions'


class LimeQuestionL10N(models.Model):
    qid = models.ForeignKey(LimeQuestion, db_column = "qid", on_delete = models.CASCADE)
    question = models.TextField()
    help = models.TextField(blank=True, null=True)
    script = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'lime_question_l10ns'
        unique_together = (('qid', 'language'),)


class LimeGroup(models.Model):
    gid = models.AutoField(primary_key=True)
    sid = models.IntegerField()
    group_order = models.IntegerField()
    randomization_group = models.CharField(max_length=20)
    grelevance = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lime_groups'

class LimeGroupL10N(models.Model):
    gid = models.ForeignKey(LimeGroup, db_column = "gid", on_delete = models.CASCADE)
    group_name = models.TextField()
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'lime_group_l10ns'
        unique_together = (('gid', 'language'),)