# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from CreateYourLaws.models import LawArticle, Commit  # , UserSession
import CreateYourLaws.models
from django.template.loader_tags import BlockNode, ExtendsNode
from difflib import SequenceMatcher


def get_path(obj):
    """ findthe path made to the object in input.
    The Object must be made from the models classes:
    - Question
    - Disclaim
    - Opinion
    - Explaination
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
        return 'law'
    elif type(obj) is CreateYourLaws.models.Commit:
        return 'com'


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
    elif obj == 'opp':
        return CreateYourLaws.models.Posopinion.objects.get(id=Id)
    elif obj == 'opn':
        return CreateYourLaws.models.Negopinion.objects.get(id=Id)
    elif obj == 'prp':
        return CreateYourLaws.models.Proposition.objects.get(id=Id)
    elif obj == 'law':
        return CreateYourLaws.models.LawArticle.objects.get(id=Id)
    elif obj == 'com':
        return CreateYourLaws.models.Commit.objects.get(id=Id)

def CreateCommit(ref, newtxt, newtitle, details, comments):
    if type(ref) is CreateYourLaws.models.LawArticle:
        commit = Commit.objects.create(
            commit_txt = CreateCommitstr(ref.text_law, newtxt),
            commit_title = CreateCommitstr(ref.title, newtitle),
            commit_details = details,
            comments = comments,
            content_object=ref,
            )
        commit.save()
    elif type(ref) is CreateYourLaws.models.Proposition:
        commit = Commit.objects.create(
            commit_txt = CreateCommitstr(ref.text_prp, newtxt),
            commit_title = CreateCommitstr(ref.title, newtitle),
            commit_details = CreateCommitstr(ref.details_prp, details),
            comments = comments,
            content_object=ref,
            )
        commit.save()


def CreateCommitstr(oldtxt,newtxt):
    """
    Commit structure: 
    list of [ tag, i1, i2, j1, j2,oldtext[i1,i2]]
    with:
        -i(n) = n(th) iteration of oldtxt
        -j(n) = n(th) iteration of newtxt
        -tag: equal, replace, delete, insert
    """
    SeqMatch= SequenceMatcher()
    SeqMatch.set_seqs(oldtxt,newtxt)
    Commit = []
    for el in SeqMatch.get_opcodes():
        comlist = list(el)
        if el[0] == "equal":
            comlist.append("")
            Commit.append(comlist)
        else:
            old = oldtxt[el[1]:el[2]]
            comlist.append(old)
            Commit.append(comlist)
    return str(Commit)


def RecoverOldComimtstr(newtxt,Commit):
    """ recover and old text from a commit"""
    oldtxt = ""
    for el in Commit:
        if el[0] == 'equal':
            oldtxt += newtxt[el[3]:el[4]]
        if el[0] == 'replace':
            oldtxt += el[5]
        if el[0] == 'delete':
            oldtxt += el[5]
    return oldtxtx

def get_box_parents(Box):
    listparents = []
    lastbox = Box
    while lastbox.rank != 1:
        parent = lastbox.block
        listparents.append((parent.title, parent.id, 2))
        lastbox = parent
    parent = Box.law_code
    listparents.append((parent.title, parent.id, 1))
    listparents.reverse()
    return listparents

def get_ref_parents(ref,typeref):
    if typeref == 'law':
        parent = ref.block
        if parent is None:
            listparents = []
        else:
            listparents = [(parent.title, parent.id, 2)]
            while parent.rank != 1:
                parent = parent.block
                listparents.append((parent.title, parent.id, 2))
        law_code = ref.law_code
        listparents.append((law_code.title, law_code.id, 1))
        fstparent = listparents[0]
        listparents.reverse()
    elif typeref == 'prp':
        listparents =[]
        fstparent = [get_model_type_in_str(ref.content_object),
                     ref.content_object.id,
                     ref.content_object.title,
                     ]
        law_code = ref.law_article.law_code
    else:
        law_code, listparents = get_path(ref)
        fstparent = listparents[0]
    return law_code, listparents, fstparent