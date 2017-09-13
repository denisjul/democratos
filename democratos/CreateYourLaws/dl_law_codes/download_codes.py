# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# #############################################################################
# ################################   Notes   ##################################
# #############################################################################
"""
1. run the script
2. acces to the codes by listofcodes: for the 'x'th code:
    listofcodes[x][0] or listofcodes[x][2].name: code's title
    listofcodes[x][1]: ref legifrance
    listofcodes[x][2]: the code

*listofcodes[x][2].contents[] will return the main titles of the codes
*listofcodes[x][2].contents[0].contents[] will return the rank 2 titles or
the Articles contained in the first main title of the code
*etc.
"""
# #############################################################################

try:
    from dl_law_codes.classe_pdf import Code_de_lois, Article, Titre, Table
    from dl_law_codes.functions import remove_piece_of_text, get_something
    from models import LawCode, LawArticle, CodeBlock
    from stock_update import SU_Article
except:
    from CreateYourLaws.dl_law_codes.classe_pdf import Code_de_lois, Article
    from CreateYourLaws.dl_law_codes.classe_pdf import Titre, Table
    from CreateYourLaws.dl_law_codes.functions import get_something
    from CreateYourLaws.dl_law_codes.functions import remove_piece_of_text
    from CreateYourLaws.models import LawCode, LawArticle
    from CreateYourLaws.models import CodeBlock, CYL_user
    from CreateYourLaws.dl_law_codes.stock_update import SU_Article

import ssl
import urllib.error
import urllib.request
import urllib.parse


def get_code_data(code_LEGITEXT, url_fail, Gov):  # 2
    """ Recover the data (titles and articles) from a specified code
    (param code LEGITEXT corresponding on Legifrance) """
    url = "https://www.legifrance.gouv.fr/affichCode.do?cidTexte="\
        + "LEGITEXT" + code_LEGITEXT
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        a = urllib.request.urlopen(url, context=ctx)
        code_source = a.read().decode("utf-8")
    except:
        url_fail.append(('code', code_LEGITEXT))
        return url_fail
    code = Code_de_lois()
    pos_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    buf_15 = ""
    list_title_open = []
    for i in range(len(code_source)):
        buf_15 += code_source[i]
        if len(buf_15) == 15:
            # --------- Code title recovering ---------------
            if buf_15 == 'd="titreTexte">':
                code.name, i = get_title_code(code_source, i)
                code.name = code.name.replace("\r", "")
                code.name = code.name.replace("\t", "")
                try:
                    Law_Code, created = LawCode.objects.get_or_create(
                        title=code.name)
                    Law_Code.updated = True
                    Law_Code.save()
                except:
                    print("Impossible to get/create the law code: ", code.name)
            # ------- paragraph title recovering ------------
            if buf_15 == '<span class="TM':
                title, i = get_title(code_source, i)
                if title.rank == 1:
                    code.contents.append(title)
                    pos_counter[2] = 0
                    list_title_open.clear()
                else:
                    for x in range(len(list_title_open) - 1, 0, -1):
                        if list_title_open[x].rank >= title.rank:
                            if list_title_open[x].rank > title.rank:
                                pos_counter[list_title_open[x].rank] = 0
                            del list_title_open[x]
                    list_title_open[-1].contents.append(title)
                pos_counter[title.rank] += 1
                try:
                    new_title, created = CodeBlock.objects.get_or_create(
                        title=title.name,
                        position=pos_counter[title.rank],
                        rank=title.rank,
                        law_code=Law_Code)
                    title.idsql = new_title.id
                    if (title.rank > 1 and
                            list_title_open[-1].idsql < title.idsql):
                        new_title.block = CodeBlock.objects.get(
                            title=list_title_open[-1].name,
                            rank=list_title_open[-1].rank,
                            id=list_title_open[-1].idsql,
                            law_code=Law_Code)
                    new_title.updated = True
                    new_title.save()
                except:
                    print("Impossible to get/create the block code",
                          " title: ", title.name,
                          "(rank: ", title.rank, ")",
                          "from: ", code.name)
                list_title_open.append(title)
            # -- Articles contained in the last paragraph Title recovering --
            if buf_15 == '="codeLienArt">':
                link, i = get_link_articles(code_source, i)
                url_fail, several_articles = get_article(link,
                                                         code.name,
                                                         new_title,
                                                         url_fail)
                for x in range(len(several_articles)):
                    try:
                        SU_Article(several_articles[x],
                                   link,
                                   new_title,
                                   Law_Code,
                                   Gov)
                    except Exception:
                        try:
                            art, created = LawArticle.objects.get_or_create(
                                autor=Gov,
                                title=several_articles[x].name,
                                law_code=Law_Code,
                                block=new_title)
                            art.updated = False
                            art.url = link
                            art.save()
                        except Exception:
                            print("Unable to create or get the instance of ",
                                  "LawArticle from",
                                  several_articles[x].name,
                                  "from law code: ",
                                  Law_Code.title)
                # Ligne suivante à surveiller si pb stockage dans les blocks
                list_title_open[-1].contents = several_articles
            buf_15 = buf_15[1:15]
    return url_fail


def get_article(link, code, block, url_fail):
    """ detect, select and copy all articles from a Legifrance page """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    contents = []
    try:
        b = urllib.request.urlopen(link, context=ctx)
        cs_article = b.read().decode("utf-8")
    except:
        url_fail.append(("article", link, code, block))
        return url_fail, contents
    new_article = Article()
    buf = ""
    for j in range(len(cs_article)):
        buf += cs_article[j]
        if len(buf) >= 21:
            if buf == '<div class="article">':
                new_article.name, j = get_something(cs_article,
                                                    '<div class="titreArt">',
                                                    '<a',
                                                    j)
                try:
                    new_article.html, j = get_something(cs_article,
                                                        'class="corpsArt">',
                                                        '</div>',
                                                        j)
                    new_article.contents = recover_article(new_article.html)
                    contents.append(new_article)
                    new_article = Article()
                except:
                    print("Légifrance trouble: impossible to get article: ",
                          new_article.name,
                          " from code: ",
                          code)
            buf = buf[1:21]
    return url_fail, contents


def recover_article(text):
    """recover the entire article (text & table parts)"""
    text = text.replace('<center>', "")
    text = text.replace('</center>', "")
    if text[0:5] == '<br/>':
        text = text[5:len(text) - 1]
    article = []
    i = 0
    buf_get_table = text[0:7]
    art_part = ""
    while i < len(text):
        if buf_get_table == "<table ":
            article.append(clean_article_text(art_part))
            art_part = ""
        elif buf_get_table == "/table>":
            i += 7
            art_part += "/table>"
            tab = Table(art_part)
            article.append(tab)
            art_part = ""
        art_part += text[i]
        i += 1
        buf_get_table = text[i:i + 7]
    article.append(clean_article_text(art_part))
    return article


def clean_article_text(text):
    """ remove all html link to keep the text """
    text = remove_piece_of_text(text, '<a', '>')
    text = text.replace('</a>', '')
    return text


def get_link_articles(code_source, i):  # 2.c
    i += 11
    buf = ""
    link = ""
    flag = True
    while flag:
        i += 1
        link += code_source[i]
        buf += code_source[i]
        if len(buf) >= 2:
            if buf == '">':
                flag = False
            buf = buf[1:2]
    link = link.replace('">', '')
    link = link.replace('&amp;', '&')
    link = "https://www.legifrance.gouv.fr/" + link
    return link, i


def get_title(code_source, i):  # 2.b
    """ record a title from a chapter, book, part, etc.
    from a law code, with his rank
    (ex:a book rank> a part rank> a chapter rank...)"""
    i += 1
    rank = int(code_source[i])
    i += 32
    buf = ""
    titre = ""
    flag = True
    while flag:
        i += 1
        titre += code_source[i]
        buf += code_source[i]
        if len(buf) >= 2:
            if buf == '</':
                flag = False
            buf = buf[1:2]
    titre = titre.replace('\n', '')
    titre = titre.replace('</', '')
    titre = titre.replace('&#13;', '')
    NewTitle = Titre(rank, titre)
    return NewTitle, i


def get_title_code(code_source, i):  # 2.a
    """ Recover the title of a law code"""
    buf = ""
    titre = ""
    flag = True
    while flag:
        i += 1
        titre += code_source[i]
        buf += code_source[i]
        if len(buf) >= 5:
            if buf == '</div' or buf == '<span':
                flag = False
            buf = buf[1:5]
    titre = titre.replace('\n', '')
    titre = titre.replace('<br/>', '')
    titre = titre.replace('</div', '')
    titre = titre.replace('<span', '')
    i += 1
    return titre, i


def get_LEGITEXT_ref(code_source, i):  # 1.1
    """ recover a Legifrance law code reference with his title
    return a tuple with """
    code_ref = ""
    title = ""
    for j in range(12):
        code_ref += code_source[i]
        i += 1
    i += 9
    while code_source[i] != '"':
        title += code_source[i]
        i += 1
    title = title.replace("&#39;", "'")
    return [title, code_ref, ""], i


def Get_codes_ref():  # 1
    """ recover all the legifrance law code reference"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://www.legifrance.gouv.fr/initRechCodeArticle.do"
    a = urllib.request.urlopen(url, context=ctx)
    code_source = a.read().decode("utf-8")
    list_of_codes = []
    buf_23 = ""
    for i in range(len(code_source)):
        buf_23 += code_source[i]
        if len(buf_23) == 23:
            if buf_23 == '<option value="LEGITEXT':
                i += 1
                ref_legitext, i = get_LEGITEXT_ref(code_source, i)
                if ref_legitext not in list_of_codes:
                    list_of_codes.append(ref_legitext)
            buf_23 = buf_23[1:len(buf_23)]
    return list_of_codes


def Get_Constitution(url_fail, Gov):  # A revoir si nouvelle constitution
    """ recover the constitution """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = ("http://www.conseil-constitutionnel.fr/conseil-constitutionnel/" +
           "francais/la-constitution/la-constitution-du-4-octobre-1958/" +
           "texte-integral-de-la-constitution-du-4-octobre-1958-" +
           "en-vigueur.5074.html")
    try:
        a = urllib.request.urlopen(url, context=ctx)
        code_source = a.read().decode("utf-8")
    except:
        url_fail.append(("constitution", url))
        return url_fail
    constitution, created = LawCode.objects.get_or_create(
        title="Constitution de la Ve Republique Française")
    constitution.updated = True
    constitution.save()
    created = False
    buf_16 = ""
    lasttitle = ""
    nb_title = 0
    flag = False
    for i in range(len(code_source)):
        buf_16 += code_source[i]
        if len(buf_16) >= 16:
            if flag and buf_16 == '<a class="link_"':
                title, i = get_something(code_source, '">', '</a>', i)
                nb_title += 1
                new_title, created = CodeBlock.objects.get_or_create(
                    title=title,
                    position=nb_title,
                    rank=1,
                    law_code=constitution)
                new_title.updated = True
                new_title.save()
                lasttitle = new_title
            elif buf_16 == '<a name="preambu':
                flag = True
                title, i = get_something(code_source, '>', '</a>', i)
                Articlesql, created = LawArticle.objects.get_or_create(
                    autor=Gov,
                    title=title,
                    law_code=constitution)
                Articlesql.updated = True
                if created:
                    text, i = get_something(code_source, '</h4>', '<h5>', i)
                    Articlesql.text_law = text
                    created = False
                Articlesql.save()
                print(Articlesql.law_code.title,
                      ': ',
                      Articlesql.title,
                      ' --> OK!')
            elif buf_16 == '<a name="article':
                title, i = get_something(code_source, '</a>', '</h', i)
                Articlesql, created = LawArticle.objects.get_or_create(
                    autor=Gov,
                    title=title,
                    law_code=constitution)
                if lasttitle != "":
                    Articlesql.block = lasttitle
                Articlesql.updated = True
                if created:
                    text, i = get_something(code_source, '>', '<h', i)
                    Articlesql.text_law = text
                    created = False
                Articlesql.save()
                print(Articlesql.law_code.title,
                      ': ',
                      Articlesql.title,
                      ' --> OK!')

            buf_16 = buf_16[1:16]
    print("constitution terminée!")
    return url_fail


def new_try(modarticle):
    """ Try again to stock an Article (in case of Légifrance
    over-requested)"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    b = urllib.request.urlopen(modarticle.link, context=ctx)
    cs_article = b.read().decode("utf-8")
    i = 0
    text, i = get_something(cs_article,
                            '<div class="titreArt">' + modarticle.title,
                            '</div>',
                            i)
    text, i = get_something(cs_article,
                            '<div class="corpsArt">',
                            '</div>',
                            i)
    artobj = recover_article(text)
    SU_Article(artobj,
               modarticle.link,
               modarticle.block,
               modarticle.law_code)


def _Main_():
    """ Main code """
    """
    # TEST CUSTOM FIELD 'TABLEFIELD'
    A = "[[1, 2, 3], [4, 5, 6, 'ton cul'], [7, 8, 9]]"
    B = TableModel(test_list=A)
    C = TableModel.objects.get(id=1)
    print(C.test_list)
    print(type(TableField().to_python(C.test_list)))
    """

    # INITIALISATION
    LawCode.objects.all().updated = False
    CodeBlock.objects.all().updated = False
    LawArticle.objects.all().updated = False
    Gov, created = CYL_user.objects.get_or_create(id=1, username="government")
    url_fail = []

    # FIRST TRY TO UPDATE EVERYTHING
    listofcodes = Get_codes_ref()
    print("c'est parti!")
    url_fail = Get_Constitution(url_fail, Gov)
    # print (listofcodes[71][0])
    """try:
        input("Press enter to continue")
    except SyntaxError:
        pass
    url_fail = get_code_data(listofcodes[71][1], url_fail, Gov)
    """
    for x in range(len(listofcodes)):
        url_fail = get_code_data(listofcodes[x][1], url_fail, Gov)

    # RECOVER ALL THE DATA FAILLED BY REQUEST ERROR
    while url_fail:
        for el in url_fail:
            if el[0] == "constitution":
                url_fail = Get_Constitution(url_fail)
            elif el[0] == "code":
                url_fail = get_code_data(el[1], url_fail)
            elif el[0] == "article":
                url_fail = get_article(el[1], el[2], el[3], url_fail)
            url_fail.remove(el)
        print(" length url_fail: ", len(url_fail))

    # 3 TRIES TO RECOVER OTHER ERRORS
    for x in range(3):
        for y in range(len(listofcodes)):
            code_to_clean = LawCode.objects.get(title=listofcodes[y][0])
            list_fail = list(
                LawArticle.objects.filter(law_code=code_to_clean,
                                          updated=False)
            )
            for el in list_fail:
                try:
                    new_try(el)
                except:
                    if x == 3:
                        print("impossible to stock",
                              el.title,
                              "from :",
                              el.law_code)

    # DELETE OBSOLETE
    list_del_LC = LawCode.objects.filter(updated=False)
    for el in list_del_LC:
        list_el_del = el.CodeBlock_set.all()
        for el2 in list_el_del:
            el2.LawArticle_set.all().delete()
        el.delete()
    CodeBlock.objects.filter(updated=False).delete()
    LawArticle.objects.filter(updated=False).delete()
