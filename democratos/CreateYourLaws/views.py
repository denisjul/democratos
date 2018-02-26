# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import ensure_csrf_cookie
from CreateYourLaws.view_functions.nav_jstree import up_nav, init_nav
from CreateYourLaws.models import (
    LawCode, LawArticle, CodeBlock, Question, Disclaim, Negopinion,
    Explaination, Posopinion, Proposition, Note,)
from CreateYourLaws.forms import (
    QuestionForm, Create_CYL_UserForm, PropositionForm, Del_account_form,
    ExplainationForm, PosopinionForm, Info_Change_Form, NegopinionForm,
    CreateNewLawForm,)
from CreateYourLaws.views_functions import (
    get_path, get_the_instance, get_model_type_in_str,)
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from CreateYourLaws.dl_law_codes.functions import get_something
from render_block import render_block_to_string
import operator


@login_required
def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    qs = LawCode.objects.all()
    lqs = list(qs)
    if request.POST:
        # print(dict(locals()))
        intro = render_block_to_string('home.html',
                                       "intro",
                                       locals())
        content = render_block_to_string('home.html',
                                         "content",
                                         locals())
        ctx = {'intro': intro,
               'content': content}
        return JsonResponse(ctx)
    else:
        return render(request, 'home.html', locals())


# ################################# nav JStree ################################

@login_required
def nav_up(request, idbox):
    """ajax for CYL nav: update the tree"""
    return up_nav(request, idbox)


@login_required
def nav_init(request):
    """ajax for CYL nav: init the tree"""
    return init_nav(request)


# ################################ UP and DOWN ################################

@login_required
@require_POST
def UP(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        # print("slug:", slug)
        typ, Id = slug.split(sep=":")
        obj = get_the_instance(typ, Id)
        ct = ContentType.objects.get_for_model(obj)
        # -------------------------------------------------------------
        # About proposition and User must have 1 position:
        # Impossible to approve a Law and a counter-proposition about the Law
        # or 2 counter-propositions about the same law
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
            data['#donlaw' + str(lart.id)] = str(x.approval_ratio)
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
def In_dat_box(request, box_type=None, box_id=None):
    """ List the blocks or articles contained in a law code or boxe """
    if request.POST:
        slug = request.POST.get('slug', None)
        box_type, box_id = slug.split(sep=":")
        box_id = int(box_id)
    if box_type == '1':
        lqs = list(
            LawArticle.objects.filter(law_code=box_id,
                                      is_lwp=False,
                                      block_id__isnull=True).order_by('id'))
        lqs += list(
            CodeBlock.objects.filter(rank=1,
                                     law_code=box_id,
                                     is_cbp=False,
                                     ).order_by('id'))
        HasLawProp = LawArticle.objects.filter(law_code=box_id,
                                               is_lwp=True,
                                               block_id__isnull=True).exists()
        HasBlocProp = CodeBlock.objects.filter(rank=1,
                                               law_code=box_id,
                                               is_cbp=True,
                                               ).exists()
        Box = LawCode.objects.get(id=box_id)
        listparents = []
    else:
        lqs = list(
            LawArticle.objects.filter(block=box_id,
                                      is_lwp=False).order_by('id'))
        lqs += list(
            CodeBlock.objects.filter(block=box_id,
                                     is_cbp=False).order_by('id'))
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
        HasLawProp = LawArticle.objects.filter(block=box_id,
                                               is_lwp=True).exists()
        HasBlocProp = CodeBlock.objects.filter(block=box_id,
                                               is_cbp=True).exists()
    print(HasLawProp, HasBlocProp)
    if request.POST:
        intro = render_block_to_string('InDatBox.html',
                                       "intro",
                                       locals())
        content = render_block_to_string('InDatBox.html',
                                         "content",
                                         locals())
        ctx = {'intro': intro,
               'content': content,
               'box_type': str(box_type),
               'box_id': str(box_id),
               }
        return JsonResponse(ctx)
    else:
        return render(request, 'InDatBox.html', locals())


@login_required
def getnewlawprops(request):
    slug = request.POST.get('slug', None)

    #    continuer ici

    ctx = {'intro': intro,
           'content': content,
           'box_type': str(box_type),
           'box_id': str(box_id)}
    return JsonResponse(ctx)


@login_required
def get_reflection(request, typeref=None, id_ref=None):
    """ View which display a reflection and its child
    reflections from its ID"""
    # Does the reflection extist?
    print("GetReflection")
    User = request.user
    if request.POST:
        slug = request.POST.get('slug', None)
        if slug is None:
            typeref = request.typeref
            id_ref = int(request.id_ref)
        else:
            typeref, id_ref = slug.split(sep=":")
            id_ref = int(id_ref)
    print("typeref", typeref)
    try:
        if typeref == 'law':
            ref = LawArticle.objects.get(id=id_ref)
        elif typeref == 'qst':
            ref = Question.objects.get(id=id_ref)
        elif typeref == 'exp':
            ref = Explaination.objects.get(id=id_ref)
        elif typeref == 'dis':
            ref = Disclaim.objects.get(id=id_ref)
        elif typeref == 'opp':
            ref = Posopinion.objects.get(id=id_ref)
        elif typeref == 'opn':
            ref = Negopinion.objects.get(id=id_ref)
        elif typeref == 'prp':
            ref = Proposition.objects.get(id=id_ref)
        print("ref: ", ref)
    except Exception:
        raise Http404
    # where is it from? path to the reflection
    if typeref == 'law':
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
    elif typeref == 'prp':
        fstparent = [get_model_type_in_str(ref.content_object),
                     ref.content_object.id,
                     ref.content_object.title,
                     ]
    else:
        law_code, list_parents = get_path(ref)
        fstparent = list_parents[0]
        print(law_code, list_parents)
    # forms initializations
    qstform = QuestionForm()
    expform = ExplainationForm()
    oppform = PosopinionForm()
    opnform = NegopinionForm()
    prpform = PropositionForm()
    print("forms loaded")
    # load all the disclaims, other proposions, opinions, comments and
    # questions about the reflection
    listexplainations = list(ref.explainations.all())
    listquestions = list(ref.questions.all())
    listcom = listexplainations
    listcom.extend(listquestions)
    listcom = sorted(listcom, key=operator.attrgetter('approval_factor'))
    listcom.reverse()
    if typeref == 'law' or typeref == 'prp':
        listposop = list(ref.posopinions.all())
        listnegop = list(ref.negopinions.all())
        if typeref == 'prp':
            listpropositions = list(ref.law_article.propositions.all())
        else:
            listpropositions = list(ref.propositions.all())
    print('Lists child reflection loaded')
    if request.POST:
        intro = render_block_to_string('GetReflection.html',
                                       "intro",
                                       locals())
        print('intro loaded')
        content = render_block_to_string('GetReflection.html',
                                         "content",
                                         locals())
        ctx = {'intro': intro,
               'content': content,
               'typeref': typeref,
               'id_ref': str(id_ref)}
        print("sucess Ajax load")
        return JsonResponse(ctx)
    else:
        print("sucess stdt load")
        return render(request, 'GetReflection.html', locals())


def PostReflection(request):  # Trouver un moyen d'avoir ID_ref
    typeform = request.POST.get('typeform', '')
    typeref = request.POST.get('typeref', '')
    place = request.POST.get('place', '')
    print("place: ",
          place,
          "\ntypeform: ",
          typeform,
          "\ntyperef: ",
          typeref)
    id_ref = int(request.POST.get('ref_id', None))
    IsModif = bool(request.POST.get('IsModif', False))
    if IsModif:
        idform = int(request.POST.get('idform', None))
    User = request.user
    ref = get_the_instance(typeref, id_ref)
    fstparent = [typeref,
                 ref.id,
                 ref.title,
                 ]
    id_ref = str(id_ref)
    # ####################  PropositionForm ###########################
    if typeform == 'prpf'and request.method == 'POST':
        print("c'est un prpf")
        prpform = PropositionForm(request.POST)
        if prpform.is_valid():
            proptitle = prpform.cleaned_data['title']
            prop = prpform.cleaned_data['text_prp']
            details_prp = prpform.cleaned_data['details_prp']
            print(proptitle, prop, details_prp)
            if isinstance(ref, LawArticle):
                lawart = ref
            else:
                lawart = ref.law_article
            if IsModif:
                prp = Proposition.objects.get(id=idform)
                prp.text_prp = prop
                prp.title = proptitle
                prp.details_prp = details_prp
                listpropositions = list(ref.propositions.all())
            else:
                if isinstance(ref, Proposition):
                    ctob = ref.law_article  # all prp must point on a law
                else:
                    ctob = ref
                prp = Proposition.objects.create(text_prp=prop,
                                                 title=proptitle,
                                                 autor=User,
                                                 details_prp=details_prp,
                                                 law_article=lawart,
                                                 content_object=ctob)
                listpropositions = list(ctob.propositions.all())
            prp.save()
            prpform = PropositionForm()
            NewSection = render_block_to_string('GetReflection.html',
                                                'content',
                                                locals())
            NewSection, trash = get_something(NewSection,
                                              '<section ' +
                                              'class="Bigproposition' +
                                              ' UpSection" id="propsection">',
                                              '</section>',
                                              0)
            ctx = {'NewSection': NewSection,
                   'section_type': "prp",
                   'tdid': ""}

    # ####################  OpinionForm #########################
    #      <---- Revoir si séparer Posop et Negop

    elif request.method == 'POST' and typeform == 'oppf':
        oppform = PosopinionForm(request.POST)
        if oppform.is_valid():
            optitle = oppform.cleaned_data['title']
            opin = oppform.cleaned_data['text_opp']
            if IsModif:
                opp = Posopinion.objects.get(id=idform)
                opp.text_opp = opin
                opp.title = optitle
            else:
                opp = Posopinion.objects.create(text_opp=opin,
                                                title=optitle,
                                                autor=User,
                                                content_object=ref)
            opp.save()
            listposop = list(ref.posopinions.all())
            oppform = PosopinionForm()
            NewSection = render_block_to_string('GetReflection.html',
                                                'content',
                                                locals())
            start = '<article class="Bigposopinion UpSection"' +\
                    ' id="posopsection">'
            NewSection, trash = get_something(NewSection,
                                              start,
                                              '</article>',
                                              0)
            ctx = {'NewSection': NewSection,
                   'section_type': "opp",
                   'tdid': ""}

    elif request.method == 'POST' and typeform == 'opnf':
        opnform = NegopinionForm(request.POST)
        if opnform.is_valid():
            optitle = opnform.cleaned_data['title']
            opin = opnform.cleaned_data['text_opn']
            if IsModif:
                opn = Negopinion.objects.get(id=idform)
                opn.text_opn = opin
                opn.title = optitle
            else:
                opn = Negopinion.objects.create(text_opn=opin,
                                                title=optitle,
                                                autor=User,
                                                content_object=ref)
            opn.save()
            listnegop = list(ref.negopinions.all())
            NewSection = render_block_to_string('GetReflection.html',
                                                'content',
                                                locals())
            start = '<article class="Bignegopinion UpSection"' +\
                    ' id="negopsection">'
            NewSection, trash = get_something(NewSection,
                                              start,
                                              '</article>',
                                              0)
            ctx = {'NewSection': NewSection,
                   'section_type': "opn",
                   'tdid': ""}

    # ####################  QuestionForm ###########################
    elif request.method == 'POST' and (typeform == 'qstf' or
                                       typeform == 'expf'):
        if typeform == 'expf':
            expform = ExplainationForm(request.POST)
            if expform.is_valid():
                exptitle = expform.cleaned_data['title']
                explain = expform.cleaned_data['text_exp']
                if IsModif:
                    exp = Explaination.objects.get(id=idform)
                    exp.text_exp = explain
                    exp.title = exptitle
                else:
                    exp = Explaination.objects.create(title=exptitle,
                                                      text_exp=explain,
                                                      autor=User,
                                                      content_object=ref)
                exp.save()
        elif typeform == 'qstf':
            qstform = QuestionForm(request.POST)
            if qstform.is_valid():
                qtitle = qstform.cleaned_data['title']
                question = qstform.cleaned_data['text_q']
                if IsModif:
                    q = Question.objects.get(id=idform)
                    q.text_q = question
                    q.title = qtitle
                else:
                    q = Question.objects.create(text_q=question,
                                                title=qtitle,
                                                autor=User,
                                                content_object=ref)
                q.save()
        listexplainations = list(ref.explainations.all())
        listquestions = list(ref.questions.all())
        listcom = listexplainations
        listcom.extend(listquestions)
        listcom = sorted(listcom,
                         key=operator.attrgetter('approval_factor'))
        expform = ExplainationForm()
        qstform = QuestionForm()
        NewSection = render_block_to_string('GetReflection.html',
                                            'content',
                                            locals())
        NewSection, trash = get_something(NewSection,
                                          '<section id="' +
                                          typeref + 'debate' + id_ref +
                                          '" class="UpSection">',
                                          '</section>',
                                          0)
        ctx = {'NewSection': NewSection,
               'section_type': typeform[0:2],
               'typeform': typeform,
               'typeref': typeref,
               'tdid': str(id_ref)}
    else:
        print("FORM NON VALIDE. ERREURE")
    if IsModif:
        ctx["message"] = "Votre réflection a bien été modifié!"
    else:
        ctx["message"] = ""
    print("end PostReflection")
    return JsonResponse(ctx)


@login_required
def list_of_reflections(request, parent_type, parent_id, list_ref_type):
    """ display the list of given reflection type from the parent obj.
    ex: list of the questions askedUWB about law article X."""
    parent = get_the_instance(parent_type, parent_id)
    if list_ref_type == 'qst':
        list_to_display = list(parent.questions.all())
    elif list_ref_type == 'exp':
        list_to_display = list(parent.explainations.all())
    elif list_ref_type == 'dis':
        list_to_display = list(parent.disclaims.all())
    elif list_ref_type == 'opp':
        list_to_display = list(parent.posopinions.all())
    elif list_ref_type == 'opn':
        list_to_display = list(parent.negopinions.all())
    elif list_ref_type == 'prp':
        list_to_display = list(parent.propositions.all())
    return render(request, 'displaylist.html', locals())


@login_required
def getchildcomments(request):
    """ View which display a reflection and its child
    reflections from its ID and typeref"""
    slug = request.POST.get('slug', None)
    typeref = slug[5:8]
    id_ref = slug[8:len(slug)]
    id_ref = int(id_ref)
    User = request.user
    print("children from", typeref, id_ref)
    message = ""
    try:
        if typeref == 'qst':   # Does the reflection extist?
            ref = Question.objects.get(id=id_ref)
        elif typeref == 'exp':
            ref = Explaination.objects.get(id=id_ref)
        fstparent = [typeref,
                     ref.id,
                     ref.title,
                     ]
        listexplainations = list(ref.explainations.all())
        listquestions = list(ref.questions.all())
        listcom = listexplainations
        listcom.extend(listquestions)
        listcom = sorted(listcom, key=operator.attrgetter('approval_factor'))
        NewSection = render_block_to_string('GetReflection.html',
                                            'content',
                                            locals())
        print("we are here")
        NewSection, trash = get_something(NewSection,
                                          '<section id="' +
                                          typeref +
                                          'debate' + str(id_ref) +
                                          '" class="UpSection">',
                                          '</section>',
                                          0)
        NewSection = '<div id="' + typeref +\
                     'debate' + str(id_ref) +\
                     '" class="UpSection">' +\
                     NewSection +\
                     '</div>'
        ctx = {'message': message,
               'newcomments': NewSection,
               'typeref': typeref,
               "idref": str(id_ref)
               }
    except Exception:
        message = "comment unfindable in DB"
        ctx = {'message': message,
               'newcomments': "",
               'typeref': typeref,
               "idref": str(id_ref)
               }
    return JsonResponse(ctx)


@login_required
def GetForm(request):
    """ Get the question or explaination form in a reflection
    page """
    modifForm = False
    name = request.GET.get('name', None)
    typeref, typeform, idref = name.split(sep=":")
    if typeform == 'qst':   # which form to load?
        form = QuestionForm()
    elif typeform == 'exp':
        form = ExplainationForm()
    NewForm = render_block_to_string('GetForm.html',
                                     "content",
                                     locals())
    ctx = {'newform': NewForm, 'typeref': typeref, "idref": idref}
    return JsonResponse(ctx)


@login_required
def ModifReflection(request):
    """ Load the form for an Autor to
    modify his own reflection content once posted"""

    if (request.method == 'POST' and
            request.POST.get('typerequest', None) == 'form'):
        IsModif = True
        typeform = request.POST.get('typeform', None)
        idform = int(request.POST.get('idform', None))
        typeref = request.POST.get('typeref', None)
        idref = int(request.POST.get('idref', None))
        obj = get_the_instance(typeform, idform)
        if typeform == 'qst':
            form = QuestionForm(initial={'title': obj.title,
                                         'text_q': obj.text_q
                                         })
        elif typeform == 'exp':
            form = ExplainationForm(initial={'title': obj.title,
                                             'text_exp': obj.text_exp
                                             })
        elif typeform == 'opp':
            form = PosopinionForm(initial={'title': obj.title,
                                           'text_opp': obj.text_opp
                                           })
        elif typeform == 'opn':
            form = NegopinionForm(initial={'title': obj.title,
                                           'text_opn': obj.text_opn
                                           })
        elif typeform == 'prp':
            form = PropositionForm(initial={'title': obj.title,
                                            'text_prp': obj.text_prp,
                                            'details_prp': obj.details_prp,
                                            })
        else:
            print("http1")
            raise Http404
        formhtml = render_to_string('GetForm.html', locals())
        ctx = {'ModifForm': formhtml,
               'typeform': typeform,
               'typeref': typeref,
               'idref': idref,
               'idform': idform,
               }
    else:
        print("http2")
        raise Http404
    return JsonResponse(ctx)


@login_required
def DeleteReflection(request):
    """ Enable the Autor or the comunity to delete a comment """
    typeref = request.POST.get('typeref', None)
    idref = int(request.POST.get('idref', None))
    obj = get_the_instance(typeref, idref)
    obj.delete()
    ctx = {'message': 'Votre commentaire a bien été supprimé'}
    return JsonResponse(ctx)


@login_required
@ensure_csrf_cookie
def CreateNewLaw(request, box_id=None):
    """ View to ask form to create a new law article """
    if request.GET:
        print(request.GET.get('slug', None))
        box = request.GET.get('slug', None)
        box_type = box[0]
        box_id = int(box[2:])
        typeform = "lawf"
        form = CreateNewLawForm()
        """
        NewHtml = render_to_string('GetForm.html',
                                   locals(),
                                   request)
        intro, trash = get_something(NewHtml,
                                     '<!-- *o* -->',
                                     "<!-- *_* -->",
                                     0)
        content, trash = get_something(NewHtml,
                                       '<!-- *X* -->',
                                       "<!-- *U* -->",
                                       0)"""
        intro = render_block_to_string('GetForm.html',
                                       "intro",
                                       locals(),
                                       request)
        content = render_block_to_string('GetForm.html',
                                         "content",
                                         locals(),
                                         request)
        ctx = {'intro': intro,
               'content': content,
               'box_type': box_type,
               'box_id': str(box_id)}
        return JsonResponse(ctx)
    else:
        return render(request, 'GetForm.html', locals())


@login_required
def ValidNewLaw(request):
    User = request.user
    typeref = "law"
    lawform = CreateNewLawForm(request.POST)
    if lawform.is_valid():
        lawtitle = lawform.cleaned_data['title']
        law_text = lawform.cleaned_data['text_law']
        law_details = lawform.cleaned_data['details_law']
        IsModif = bool(request.POST.get('IsModif', False))
        if IsModif:
            idform = int(request.POST.get('idform', None))
            ref = LawArticle.objects.get(id=idform)
            ref.text_law = prop
            ref.title = proptitle
            ref.details_law = details_prp
            listpropositions = list(ref.propositions.all())
        else:
            boxid = int(request.POST.get('box_id', None))
            boxtype = request.POST.get('box_type', None)
            print(boxtype, boxid)
            if boxtype == 'D':
                box = None
                Law_code = LawCode.objects.get(id=boxid)
            elif boxtype == 'E':
                box = CodeBlock.objects.get(id=boxid)
                Law_code = box.law_code
            else:
                print("boxtype error")
                raise Http404
            ref = LawArticle.objects.create(text_law=law_text,
                                            title=lawtitle,
                                            autor=User,
                                            is_lwp=True,
                                            law_code=Law_code,
                                            details_law=law_details,
                                            block=box)
        ref.save()
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
        # forms initializations
        qstform = QuestionForm()
        expform = ExplainationForm()
        oppform = PosopinionForm()
        opnform = NegopinionForm()
        prpform = PropositionForm()
        # load all the disclaims, other proposions, opinions, comments and
        # questions about the reflection
        listexplainations = list(ref.explainations.all())
        listquestions = list(ref.questions.all())
        listcom = listexplainations
        listcom.extend(listquestions)
        listcom = sorted(listcom, key=operator.attrgetter('approval_factor'))
        listcom.reverse()
        listposop = list(ref.posopinions.all())
        listnegop = list(ref.negopinions.all())
        listpropositions = list(ref.propositions.all())
        intro = render_block_to_string('GetReflection.html',
                                       "intro",
                                       locals(),
                                       request)
        content = render_block_to_string('GetReflection.html',
                                         "content",
                                         locals(),
                                         request)
        ctx = {'intro': intro,
               'content': content,
               'typeref': typeref,
               'typeform': "lawf",
               'id_ref': str(ref.id),
               'message': "Votre proposition de loi a bien été ajoutée."}
        return JsonResponse(ctx)
    else:
        raise Http404


@login_required
def create_new_box():
    """ View to create a new Law Code or codeblock """
    pass
