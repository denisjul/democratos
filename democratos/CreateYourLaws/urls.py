# -*-coding: utf-8 -*-

from django.urls import path, include
from . import views, user_manage
from django.conf import settings
from django.conf.urls.static import static
from CreateYourLaws.forms import Create_CYL_UserForm


urlpatterns = [
    path('', views.home, name='home'),
    path('nav_up/<str:idbox>',
         views.nav_up,
         name="nav_up"),
    path('nav_init', views.nav_init, name="nav_init"),
    path('UP', views.UP, name="UP"),
    path('DOWN', views.DOWN, name="DOWN"),
    path('checkbox', views.Checkbox, name="checkbox"),
    path('profile', views.view_profile, name="profile"),
    path('InDatBox', views.In_dat_box, name='InDatBox'),
    path('Reflection/<str:typeref>/<int:id_ref>',
         views.get_reflection,
         name='Reflection'),
    path('reflection',
         views.get_reflection,
         name='reflection'),
    path('childcomments',
         views.getchildcomments,
         name='chilcomments'),
    path('CreateNewLaw',
         views.CreateNewLaw,
         name='CreateNewLaw'),
    path('ValidNewLaw',
         views.ValidNewLaw,
         name='ValidNewLaw'),
    path('DeleteReflection',
         views.DeleteReflection,
         name='DeleteReflection'),
    path('ModifReflection',
         views.ModifReflection,
         name='ModifReflection'),
    path('GetForm',
         views.GetForm,
         name='GetForm'),
    path('postreflection', views.PostReflection, name='PostReflection'),
    path('listref/<str:parent_type>/<int:parent_id>/<str:list_ref_type>',
         views.list_of_reflections,
         name='list_ref'),
    path('accounts/', include('registration.backends.default.urls')),
    path('captcha/', include('captcha.urls')),
    path('accounts/register/',
         user_manage.Create_User.as_view(form_class=Create_CYL_UserForm),
         name='registration_register'),
    path('info/change/done', views.info_change_done, name="InfoChangeDone"),
]
"""+ static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
"""
