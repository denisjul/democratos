# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from CreateYourLaws.models import LawCode, LawArticle
from CreateYourLaws.models import CodeBlock, Question, Disclaim
from CreateYourLaws.models import Explaination, Opinion, Proposition
from CreateYourLaws.models import Note
from CreateYourLaws.forms import QuestionForm, Create_CYL_UserForm
from CreateYourLaws.forms import PropositionForm, Del_account_form
from CreateYourLaws.forms import ExplainationForm, OpinionForm, DisclaimForm
from CreateYourLaws.forms import Info_Change_Form
from CreateYourLaws.views_functions import get_path, get_the_instance
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse


@login_required
def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    qs = LawCode.objects.all()
    lqs = list(qs)
    return render(request, 'home.html', locals())


# ################################# nav JStree ################################

@login_required
def nav_up(request, idbox):
    """ajax for CYL nav: update the tree"""
    id_box = int(idbox[1:len(idbox)])
    children = []
    JSON_obj = []
    if idbox[0] == 'A':
        listArticle = list(
            LawArticle.objects.filter(law_code=id_box,
                                      block_id__isnull=True).order_by('id'))
    else:
        listArticle = list(
            LawArticle.objects.filter(block=id_box).order_by('id'))
    if listArticle:
        for el in listArticle:
            children.append(('C' + str(el.id),
                             el.title,
                             "GetReflection",
                             'loi:' + str(el.id),
                             False))
    if idbox[0] == 'A':
        listBlock = list(
            CodeBlock.objects.filter(rank=1, law_code=id_box).order_by('id'))
    else:
        listBlock = list(
            CodeBlock.objects.filter(block=id_box).order_by('id'))
    if listBlock:
        for el in listBlock:
            children.append(('B' + str(el.id),
                             el.title,
                             "InDatBox",
                             '2:' + str(el.id),
                             True))
    for elem in children:
        # 'B' in the 'id' param inform that this is a Code BLock
        JSON_obj.append({'id': elem[0],
                         'text': elem[1],
                         'a_attr': {'class': elem[2],
                                    'name': elem[3]},
                         'children': elem[4]})
    return JsonResponse(JSON_obj, safe=False)


@login_required
def nav_init(request):
    """ajax for CYL nav: init the tree"""
    law_codes = list(LawCode.objects.all())
    JSON_obj = []
    for i, el in enumerate(law_codes):
        # 'A' in the 'id' param inform that this is a Law code
        JSON_obj.append({'id': 'A' + str(el.id),
                         'text': el.title,
                         'a_attr': {"class": "InDatBox",
                                    "name": "1:" + str(el.id)},
                         'children': True})
    return JsonResponse(JSON_obj, safe=False)


# ################################ UP and DOWN ################################

@login_required
@require_POST
def UP(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        typ, Id = slug.split(sep=":")
        obj = get_the_instance(typ, Id)
        ct = ContentType.objects.get_for_model(obj)
        # -------------------------------------------------------------
        # About proposition and User must have 1 position:
        # Impossible to approve a Law and a counter-proposition about the Law
        # or 2 counter-proposition about the same law
        # -------------------------------------------------------------
        data = {}
        if isinstance(obj, Proposition):
            try:
                note = Note.objects.get(user=user,
                                        content_type=ct,
                                        object_id=obj.id)
                if note.approve:
                    getit = True
                else:
                    getit = False
            except Exception:
                getit = False
            listprop = list(Proposition.objects.filter(
                law_article=obj.law_article))
            for x in listprop:
                data['#donprp' + str(x.id)] = str(x.approval_ratio)
                x.notes.filter(user=user, approve=True).delete()
            lart = obj.law_article
            data['#donloi' + str(lart.id)] = str(x.approval_ratio)
            lart.notes.filter(user=user, approve=True).delete()
        elif isinstance(obj, LawArticle):
            getit = False
            listprop = list(Proposition.objects.filter(
                law_article=obj))
            for x in listprop:
                data['#donprp' + str(x.id)] = str(x.approval_ratio)
                x.notes.filter(user=user, approve=True).delete()
        else:
            getit = False
        # -------------------------------------------------------------
        note, created = Note.objects.get_or_create(user=user,
                                                   content_type=ct,
                                                   object_id=obj.id)
        if (created is False and note.approve) or getit:
            message = "Vous approuvez déjà cette réflexion."\
                + "\nVous ne pouvez approuver ou"\
                + " désapprouver qu'une seule fois une réflexion."\
                + "\nVous pouvez Cependant changer "\
                + "d'avis autant de fois que vous voulez."
        else:
            message = ""
        note.approve = True
        note.save()
    obj = get_the_instance(typ, Id)
    ctx = {'message': message,
           'approb': str(obj.approval_ratio),
           'data': data}
    return JsonResponse(ctx)


@login_required
@require_POST
def DOWN(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        typ, Id = slug.split(sep=":")
        obj = get_the_instance(typ, Id)
        ct = ContentType.objects.get_for_model(obj)
        note, created = Note.objects.get_or_create(user=user,
                                                   content_type=ct,
                                                   object_id=obj.id)
        if created is False and note.approve is False:
            message = "Vous désapprouvez déjà cette réflexion."\
                + "\nVous ne pouvez approuver ou"\
                + " désapprouver qu'une seule fois une réflexion."\
                + "\nVous pouvez Cependant changer "\
                + "d'avis autant de fois que vous voulez."
        else:
            message = ""
        note.approve = False
        note.save()
    obj = get_the_instance(typ, Id)
    ctx = {'message': message, 'approb': str(obj.approval_ratio)}
    return JsonResponse(ctx)


# #################################  User  ####################################

def Create_User(request):
    """ Use to create a new User"""
    registered = False
    if request.method == 'POST':
        user_form = Create_CYL_UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
    else:
        user_form = Create_CYL_UserForm()
    return render(request, 'registration.html', locals())


def Checkbox(request):  # A revoir
    print('FONCTION CALLED')
    if request.method == 'POST':
        typeref = request.POST.get('typeref', None)
        ref_id = request.POST.get('ref_id', None)
        checked = request.POST.get('check', None)
    ctx = {}
    return JsonResponse(ctx)


@login_required
def info_change_done(request,
                     template_name='registration/info_change_done.html',
                     extra_context=None):
    """ triggered when a user changed his own infos successfuly """
    context = {
        'title': _('Info change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)


@login_required
def view_profile(request, set_var="info"):
    """ """
    if request.method == 'POST' and 'infochangebut' in request.POST:
        infochangeform = Info_Change_Form(user=request.user,
                                          data=request.POST)
        set_var = "info"
        if infochangeform.is_valid():
            infochangeform.save()
            return redirect('/CYL/info/change/done')
    else:
        infochangeform = Info_Change_Form(user=request.user)
    if request.method == 'POST' and 'pwdchangebut' in request.POST:
        pwdchangeform = PasswordChangeForm(user=request.user,
                                           data=request.POST)
        set_var = "pwd"
        if pwdchangeform.is_valid():
            pwdchangeform.save()
            update_session_auth_hash(request, pwdchangeform.user)
            return redirect('/CYL/accounts/password/change/done')
    else:
        pwdchangeform = PasswordChangeForm(user=request.user)
    if request.method == 'POST' and 'delaccountbut'in request.POST:
        del_form = Del_account_form(request.POST)
        set_var = "del"
        if del_form.is_valid(request.user):
            request.user.delete()
            return redirect('/CYL/accounts/login')
    else:
        del_form = Del_account_form()
    return render(request, 'account_set.html', locals())

# ############################# Interaction  ##################################


@login_required
def In_dat_box(request):
    """ List the blocks or articles contained in a law code or boxe """
    slug = request.POST.get('slug', None)
    box_type, box_id = slug.split(sep=":")
    box_id = int(box_id)
    if box_type == '1':
        lqs = list(
            LawArticle.objects.filter(law_code=box_id,
                                      block_id__isnull=True).order_by('id'))
        lqs += list(
            CodeBlock.objects.filter(rank=1, law_code=box_id).order_by('id'))
        Box = LawCode.objects.get(id=box_id)
        listparents = []
    else:
        lqs = list(
            LawArticle.objects.filter(block=box_id).order_by('id'))
        lqs += list(
            CodeBlock.objects.filter(block=box_id).order_by('id'))
        Box = CodeBlock.objects.get(id=box_id)
        listparents = []
        lastbox = Box
        while lastbox.rank != 1:
            parent = lastbox.block
            listparents.append((parent.title, parent.id, 2))
            lastbox = parent
        parent = Box.law_code
        listparents.append((parent.title, parent.id, 1))
        listparents.reverse()
    intro = render_to_string('intro_InDatBox.html', locals())
    content = render_to_string('content_InDatBox.html', locals())
    ctx = {'intro': intro, 'content': content}
    return JsonResponse(ctx)


@login_required
def get_reflection(request):
    """ View which display a reflection and its child
    reflections from its ID"""
    # Does the reflection extist?
    slug = request.POST.get('slug', None)
    typeref, id_ref = slug.split(sep=":")
    id_ref = int(id_ref)
    try:
        if typeref == 'loi':
            ref = LawArticle.objects.get(id=id_ref)
        elif typeref == 'qst':
            ref = Question.objects.get(id=id_ref)
        elif typeref == 'exp':
            ref = Explaination.objects.get(id=id_ref)
        elif typeref == 'dis':
            ref = Disclaim.objects.get(id=id_ref)
        elif typeref == 'opn':
            ref = Opinion.objects.get(id=id_ref)
        elif typeref == 'prp':
            ref = Proposition.objects.get(id=id_ref)
    except Exception:
        raise Http404
    # where is it from? path to the reflection
    if typeref == 'loi':
        parent = ref.block
        if parent is None:
            listparents = []
        else:
            listparents = [(parent.title, parent.id, 2)]
            while parent.rank != 1:
                parent = parent.block
                listparents.append((parent.title, parent.id, 2))
        parent = ref.law_code
        listparents.append((parent.title, parent.id, 1))
        listparents.reverse()
    # ######## elif typeref == 'prop'
    else:
        law_code, list_parents = get_path(ref)
    """
    user_session = UserSession.objects.get(
        session_id=request.session.session_key)
    User = user_session.user
    """
    User = request.user
    # forms initializations
    if request.method == 'POST' and 'btnqform' in request.POST:
        qform = QuestionForm(request.POST)
        if qform.is_valid():
            qtitle = qform.cleaned_data['title']
            question = qform.cleaned_data['text_q']
            q = Question.objects.create(text_q=question,
                                        title=qtitle,
                                        autor=User,
                                        content_object=ref)
            q.save()
    else:
        qform = QuestionForm()
    if request.method == 'POST' and 'btnexpform' in request.POST:
        expform = ExplainationForm(request.POST)
        if expform.is_valid():
            exptitle = expform.cleaned_data['title']
            explain = expform.cleaned_data['text_exp']
            exp = Explaination.objects.create(title=exptitle,
                                              text_exp=explain,
                                              autor=User,
                                              content_object=ref)
            exp.save()
    else:
        expform = ExplainationForm()
    if typeref == 'exp' or typeref == 'opn' or typeref == 'dis':
        if request.method == 'POST' and 'btndisform' in request.POST:
            disform = DisclaimForm(request.POST)
            if disform.is_valid():
                distitle = disform.cleaned_data['title']
                distext = disform.cleaned_data['text_dis']
                disc = Disclaim.objects.create(title=distitle,
                                               text_dis=distext,
                                               autor=User,
                                               content_object=ref).save()
        else:
            disform = DisclaimForm()
    if typeref == 'loi' or typeref == 'prp':
        if request.method == 'POST' and 'btnopform' in request.POST:
            opform = OpinionForm(request.POST)
            if opform.is_valid():
                pos = opform.cleaned_data['positive']
                optitle = opform.cleaned_data['title']
                opin = opform.cleaned_data['text_op']
                op = Opinion.objects.create(text_op=opin,
                                            title=optitle,
                                            positive=pos,
                                            autor=User,
                                            content_object=ref)
                op.save()
        else:
            opform = OpinionForm()
        if request.method == 'POST' and 'propform' in request.POST:
            propform = PropositionForm(request.POST)
            if propform.is_valid():
                proptitle = propform.cleaned_data['title']
                prop = propform.cleaned_data['text_prop']
                if isinstance(ref, LawArticle):
                    lawart = ref
                else:
                    lawart = ref.law_article
                prp = Proposition.objects.create(text_prop=prop,
                                                 title=proptitle,
                                                 autor=User,
                                                 law_article=lawart,
                                                 content_object=ref)

                prp.save()
        else:
            propform = PropositionForm()

    # load all the disclaims, other proposions, opinions, comments and
    # questions about the reflection
    listexplainations = list(ref.explainations.all())
    listquestions = list(ref.questions.all())
    if typeref == 'exp' or typeref == 'opn' or typeref == 'dis':
        listdisclaims = list(ref.disclaims.all())
    if typeref == 'loi' or typeref == 'prp':
        listposop = list(ref.opinions.filter(positive=True))
        listnegop = list(ref.opinions.filter(positive=False))
        listpropositions = list(ref.propositions.all())
    intro = render_to_string('intro_reflec.html', locals())
    content = render_to_string('content_reflec.html', locals())
    ctx = {'intro': intro, 'content': content}
    return JsonResponse(ctx)


def PostAProp(request):  # Trouver un moyen d'avoir ID_ref
    typeref = request.POST.get('typeref', '')
    idref = request.POST.get('ref_id', '')
    if typeref == 'prp':
        ref = Proposition.objects.get(
                id=idref
                )
    else:
        ref = LawArticle.objects.get(
                id=request.POST.get('ref_id', '')
                )
    if request.method == 'POST':
        propform = PropositionForm(request.POST)
        print(propform.is_valid())
        if propform.is_valid():
            print("hello! Is it me you are looking for?")
            proptitle = propform.cleaned_data['title']
            prop = propform.cleaned_data['text_prop']
            if isinstance(ref, LawArticle):
                lawart = ref
            else:
                lawart = ref.law_article
            prp = Proposition.objects.create(text_prop=prop,
                                             title=proptitle,
                                             autor=User,
                                             law_article=lawart,
                                             content_object=ref)
            prp.save()
    else:
        propform = PropositionForm()
    listpropositions = list(ref.propositions.all())
    NewPropSection = render_to_string('UpPropSection.html', locals())
    ctx = {'proposition': NewPropSection}
    return JsonResponse(ctx)


@login_required
def list_of_reflections(request, parent_type, parent_id, list_ref_type):
    """ display the list of given reflection type from the parent obj.
    ex: list of the questions asked about law article X."""
    parent = get_the_instance(parent_type, parent_id)
    if list_ref_type == 'qst':
        list_to_display = list(parent.questions.all())
    elif list_ref_type == 'exp':
        list_to_display = list(parent.explainations.all())
    elif list_ref_type == 'dis':
        list_to_display = list(parent.disclaims.all())
    elif list_ref_type == 'opv':
        list_to_display = list(parent.opinions.filter(positive=True))
        positif = True
    elif list_ref_type == 'opx':
        list_to_display = list(parent.opinions.filter(positive=False))
        positif = False
    elif list_ref_type == 'prp':
        list_to_display = list(parent.propositions.all())
    return render(request, 'displaylist.html', locals())


@login_required
def create_new_article():
    """ View to create a new article """
    pass


@login_required
def create_new_box():
    """ View to create a new Law Code or codeblock """
    pass


def testview(request):
    return render(request, 'test.html', locals())
