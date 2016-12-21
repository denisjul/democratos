# -*- coding: utf-8 -*-

from __future__ import unicode_literals
try:
    from dl_law_codes.classe_pdf import Table
    from models import LawArticle
except:
    from CreateYourLaws.dl_law_codes.classe_pdf import Table
    from CreateYourLaws.models import LawArticle


def SU_Article(NewArticle, link, container, Law_Code, Gov):
    """ Ad the new Article in the DB"""
    NewArticlehtml = ""
    for x in NewArticle.contents:
        if isinstance(x, Table):
            NewArticlehtml += x.html
        else:
            NewArticlehtml += x
    Articlesql, created = LawArticle.objects.get_or_create(
        autor=Gov,
        title=NewArticle.name,
        law_code=Law_Code,
        block=container)
    Articlesql.url = link
    if created:
        Articlesql.text_law = NewArticlehtml
        Articlesql.updated = True
        Articlesql.save()
    else:
        if Articlesql.html != NewArticlehtml:
            Articlesql.autor = Gov
            Articlesql.title = NewArticle.name
            Articlesql.text_law = NewArticlehtml
            Articlesql.law_code = Law_Code
            Articlesql.block = container
            Articlesql.save()
        Articlesql.updated = True
        Articlesql.save()
    print(Articlesql.law_code.title,
          ': ',
          Articlesql.title,
          ' --> OK!')
