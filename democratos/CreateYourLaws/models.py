# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from datetime import date

###############################################################################
# ########################## Classes made for users ######################### #
###############################################################################


class CYL_user(AbstractUser):
    date_of_birth = models.DateField(default=date.today)
    # elector_number = models.IntegerField()
    # digital_print = models.ImageField()
    # contacts = models.ManyToManyField('self')


class Note(models.Model):
    user = models.ForeignKey(CYL_user, on_delete=models.CASCADE)
    approve = models.NullBooleanField()
    content_type = models.ForeignKey(ContentType,
                                     null=True,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


"""  OBSOLETE?
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)
"""

###############################################################################
# #################### Classes made for website ############################# #
###############################################################################


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Reflection(models.Model):
    autor = models.ForeignKey('CYL_user',
                              on_delete=models.SET(get_sentinel_user),
                              null=True)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    approval_factor = models.FloatField(default=0)
    approval_ratio = models.FloatField(default=0)
    posted = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    notes = GenericRelation(Note)
    content_type = models.ForeignKey(ContentType,
                                     null=True,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        ordering = ['-approval_factor', '-update']


class Question(Reflection):
    text_q = RichTextField()
    explainations = GenericRelation('Explaination')
    questions = GenericRelation('self')
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)


class Disclaim(Reflection):
    text_dis = RichTextField()
    questions = GenericRelation(Question)
    explainations = GenericRelation('Explaination')
    disclaims = GenericRelation('self')
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)
    nb_dis = models.IntegerField(default=0)


class Explaination(Reflection):
    text_exp = RichTextField()
    questions = GenericRelation(Question)
    explainations = GenericRelation('self')
    disclaims = GenericRelation(Disclaim)
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)
    nb_dis = models.IntegerField(default=0)


class Posopinion(Reflection):
    text_opp = RichTextField()
    questions = GenericRelation(Question)
    explainations = GenericRelation(Explaination)
    disclaims = GenericRelation(Disclaim)
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)
    nb_dis = models.IntegerField(default=0)


class Negopinion(Reflection):
    text_opn = RichTextField()
    questions = GenericRelation(Question)
    explainations = GenericRelation(Explaination)
    disclaims = GenericRelation(Disclaim)
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)
    nb_dis = models.IntegerField(default=0)


class Proposition(Reflection):
    text_prp = RichTextField()
    details_prp = RichTextField()
    law_article = models.ForeignKey('LawArticle',
                                    on_delete=models.CASCADE)
    questions = GenericRelation(Question)
    explainations = GenericRelation(Explaination)
    posopinions = GenericRelation(Posopinion)
    negopinions = GenericRelation(Negopinion)
    propositions = GenericRelation('self')
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)
    nb_posop = models.IntegerField(default=0)
    nb_negop = models.IntegerField(default=0)


###############################################################################
# ############# Classes linked to law codes architecture #################### #
###############################################################################


class LawArticle(Reflection):
    url = models.URLField(max_length=1000, blank=True)
    text_law = RichTextField()
    law_code = models.ForeignKey('LawCode', on_delete=models.CASCADE)
    block = models.ForeignKey(
        'CodeBlock',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    updated = models.BooleanField(default='True')
    questions = GenericRelation(Question)
    explainations = GenericRelation(Explaination)
    posopinions = GenericRelation(Posopinion)
    negopinions = GenericRelation(Negopinion)
    propositions = GenericRelation(Proposition)
    nb_exp = models.IntegerField(default=0)
    nb_q = models.IntegerField(default=0)
    nb_posop = models.IntegerField(default=0)
    nb_negop = models.IntegerField(default=0)
    nb_prop = models.IntegerField(default=0)
    # is law prop (NewLaw)?
    is_lwp = models.BooleanField(default=False)
    details_law = RichTextField(default='')


class LawCode(models.Model):
    title = models.CharField(max_length=300)
    updated = models.BooleanField(default='True')
    lastupdate = models.DateTimeField(auto_now=True,
                                      verbose_name="Last update date")


class CodeBlock(models.Model):
    title = models.CharField(max_length=300)
    position = models.IntegerField()
    rank = models.IntegerField()
    updated = models.BooleanField(default='True')
    law_code = models.ForeignKey('LawCode', on_delete=models.CASCADE)
    block = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    lastupdate = models.DateTimeField(auto_now=True,
                                      verbose_name="Last update date")
    # is new code block proposition?
    is_cdp = models.BooleanField(default=False)
