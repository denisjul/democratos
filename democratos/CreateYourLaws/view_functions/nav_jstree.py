from django.http import JsonResponse
from CreateYourLaws.models import (
    LawCode, LawArticle, CodeBlock)


def up_nav(request, idbox):
    """ajax for CYL nav: update the tree
    note:
    - A: the node is a Law Code
    - B: the node is a code bloc
    - C: the node is a Law Article
    - D: the node is a New Law proposition directly for a Law Code
    - E: the node is a New Law proposition for a specific Codeblock
    - F: the node is a code block proposition directly for a Law Code
    - G: the node is a code block proposition for a specific Codeblock
    - H: Create New Law
    - I: Create New Boxes
    """
    idbox = request.GET.get("id")
    id_box = int(idbox[1:len(idbox)])
    children = []
    JSON_obj = []
    if idbox[0] == 'A' or idbox[0] == 'B':
        # Get all the current legislation and add link to prop
        if idbox[0] == 'A':  # If we are directly in a Lawcode not Codeblock
            listArticle = list(
                LawArticle.objects.filter(law_code=id_box,
                                          block_id__isnull=True,
                                          is_lwp=False).order_by('id'))
            typeboxnexlaw = 'D'
            typeboxnexbox = 'F'
        elif idbox[0] == 'B':
            listArticle = list(
                LawArticle.objects.filter(block=id_box,
                                          is_lwp=False).order_by('id'))
            typeboxnexlaw = 'E'
            typeboxnexbox = 'G'
        if listArticle:
            for el in listArticle:
                children.append(('C' + str(el.id),
                                 el.title,
                                 "GetReflection",
                                 'law:' + str(el.id),
                                 False))
        if idbox[0] == 'A':
            listBlock = list(
                CodeBlock.objects.filter(rank=1,
                                         law_code=id_box).order_by('id'))
        elif idbox[0] == 'B':
            listBlock = list(
                CodeBlock.objects.filter(block=id_box).order_by('id'))
        if listBlock:
            for el in listBlock:
                children.append(('B' + str(el.id),
                                 el.title,
                                 "InDatBox",
                                 '2:' + str(el.id),
                                 True))
        children.append((typeboxnexlaw + str(id_box),
                         'Voir les propositions de nouvelles lois ' +
                         'pour cet emplacement',
                         'GetNewLaws',
                         idbox[0] + ':' + str(id_box),
                         True))
        children.append((typeboxnexbox + str(id_box),
                         'Voir les propositions sous-groupement de loi ' +
                         'pour cet emplacement',
                         'GetNewBoxes',
                         idbox[0] + ':' + str(id_box),
                         True))
    if idbox[0] == 'D' or idbox[0] == 'E':
        # Get the New law propotions
        if idbox[0] == 'D':  # If we are directly in a Lawcode not Codeblock
            listArticle = list(
                LawArticle.objects.filter(law_code=id_box,
                                          block_id__isnull=True,
                                          is_lwp=True).order_by('id'))
        elif idbox[0] == 'E':
            listArticle = list(
                LawArticle.objects.filter(block=id_box,
                                          is_lwp=True).order_by('id'))
        if listArticle:
            for el in listArticle:
                children.append(('C' + str(el.id),
                                 el.title,
                                 "GetReflection",
                                 'law:' + str(el.id),
                                 False))
        children.append(('H'+str(id_box),
                         'Créer une loi à cet emplacement',
                         'CreateNewLaw',
                         idbox[0] + ':' + str(id_box),
                         False))
    if idbox[0] == 'F' or idbox[0] == 'G':
        # + open a Newbox to add <--------------------------------
        if idbox[0] == 'F':
            listBlock = list(
                CodeBlock.objects.filter(rank=1,
                                         law_code=id_box,
                                         is_cbp=True).order_by('id'))
        elif idbox[0] == 'G':
            listBlock = list(
                CodeBlock.objects.filter(block=id_box,
                                         is_cbp=True).order_by('id'))
        if listBlock:
            for el in listBlock:
                children.append(('G' + str(el.id),
                                 el.title,
                                 "InDatBox",
                                 '2:' + str(el.id),
                                 True))
        children.append(('I'+str(id_box),
                         'Proposer un un sous-groupement de loi à' +
                         ' cet emplacement',
                         'CreateNewBox',
                         idbox[0] + ':' + str(id_box),
                         False))
    for elem in children:
        # 'B' in the 'id' param inform that this is a Code BLock
        JSON_obj.append({'id': elem[0],
                         'text': elem[1],
                         'a_attr': {'class': elem[2],
                                    'name': elem[3],
                                    },
                         'children': elem[4]})
    return JsonResponse(JSON_obj, safe=False)


def init_nav(request):
    """ajax for CYL nav: init the tree"""
    law_codes = list(LawCode.objects.all())
    JSON_obj = []
    for i, el in enumerate(law_codes):
        # 'A' in the 'id' param inform that this is a Law code
        JSON_obj.append({'id': 'A' + str(el.id),
                         'text': el.title,
                         'a_attr': {"class": "InDatBox",
                                    "name": "1:" + str(el.id),
                                    "get_new_laws": "False",
                                    "get_new_boxes": "False",
                                    },
                         'children': True})
    return JsonResponse(JSON_obj, safe=False)