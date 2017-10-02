# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from CreateYourLaws.models import LawArticle  # , UserSession
import CreateYourLaws.models
from django.template.loader_tags import BlockNode, ExtendsNode


def get_path(obj):
    """ findthe path made to the object in input.
    The Object must be made from the models classes:
    - Question
    - Disclaim
    - Opinion
    - Explaination
    - Disclaim
    Return list of parents ugit openclassroomntil law article & law code """

    parent = obj.content_type.model_class().objects.get(id=obj.object_id)
    if parent.title is not None:
        list_parents = [(get_model_type_in_str(parent),
                         parent.id,
                         parent.title)]
    else:
        text = get_ref_text(obj)
        list_parents = [(get_model_type_in_str(parent),
                         parent.id,
                         text)]
    while isinstance(parent, LawArticle) is False:
        parent = parent.content_type.model_class().objects.get(
            id=parent.object_id)
        if parent.title is not None:
            list_parents.append((get_model_type_in_str(parent),
                                 parent.id,
                                 parent.title))
        else:
            text = get_ref_text(obj)
            list_parents.append((get_model_type_in_str(parent),
                                 parent.id,
                                 text))
    list_parents.reverse()
    LawCode = parent.law_code
    return LawCode, list_parents


def get_model_type_in_str(obj):
    """ Return the model type of obj in str for urls"""
    if type(obj) is CreateYourLaws.models.Question:
        return 'qst'
    elif type(obj) is CreateYourLaws.models.Explaination:
        return 'exp'
    elif type(obj) is CreateYourLaws.models.Disclaim:
        return 'dis'
    elif type(obj) is CreateYourLaws.models.Posopinion:
        return 'opp'
    elif type(obj) is CreateYourLaws.models.Negopinion:
        return 'opn'
    elif type(obj) is CreateYourLaws.models.Proposition:
        return 'prp'
    elif type(obj) is CreateYourLaws.models.LawArticle:
        return 'loi'


def get_ref_text(obj):
    """ Necessity because each reflection has its own
    text appelation (CKeditor trouble)"""
    if type(obj) is CreateYourLaws.models.Question:
        return obj.text_q
    elif type(obj) is CreateYourLaws.models.Explaination:
        return obj.text_exp
    elif type(obj) is CreateYourLaws.models.Disclaim:
        return obj.text_dis
    elif type(obj) is CreateYourLaws.models.Posopinion:
        return obj.text_opp
    elif type(obj) is CreateYourLaws.models.Negopinion:
        return obj.text_opn
    elif type(obj) is CreateYourLaws.models.Proposition:
        return obj.text_prop
    elif type(obj) is CreateYourLaws.models.LawArticle:
        return obj.text


def get_the_instance(obj, Id):
    """ From the class in string, and Id, get the corresponding instance"""
    if obj == 'qst':
        return CreateYourLaws.models.Question.objects.get(id=Id)
    elif obj == 'exp':
        return CreateYourLaws.models.Explaination.objects.get(id=Id)
    elif obj == 'dis':
        return CreateYourLaws.models.Disclaim.objects.get(id=Id)
    elif obj == 'opn':
        return CreateYourLaws.models.Posopinion.objects.get(id=Id)
    elif obj == 'opn':
        return CreateYourLaws.models.Negopinion.objects.get(id=Id)
    elif obj == 'prp':
        return CreateYourLaws.models.Proposition.objects.get(id=Id)
    elif obj == 'loi':
        return CreateYourLaws.models.LawArticle.objects.get(id=Id)


# A revoir <----------------------------------------------
"""
def delete_user_sessions(user):
    user_sessions = UserSession.objects.filter(user=user)
    for user_session in user_sessions:
        user_session.session.delete()"""
