# -*-coding: utf-8 -*-

from django.conf.urls import url, include
from . import views, user_manage
from django.conf import settings
from django.conf.urls.static import static
from CreateYourLaws.forms import Create_CYL_UserForm


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^nav_up/(?P<idbox>\w+)$',
        views.nav_up,
        name="nav_up"),
    url(r'^nav_init$', views.nav_init, name="nav_init"),
    url(r'^UP$', views.UP, name="UP"),
    url(r'^DOWN$', views.DOWN, name="DOWN"),
    url(r'^checkbox$', views.Checkbox, name="checkbox"),
    url(r'^profile$', views.view_profile, name="profile"),
    url(r'^InDatBox$', views.In_dat_box, name='InDatBox'),
    url(r'^Reflection/(?P<typeref>\w{3})/(?P<id_ref>\d+)$',
        views.get_reflection,
        name='Reflection'),
    url(r'^reflection$',
        views.get_reflection,
        name='reflection'),
    url(r'^childcomments$',
        views.getchildcomments,
        name='chilcomments'),
    url(r'^DeleteReflection$',
        views.DeleteReflection,
        name='DeleteReflection'),
    url(r'^GetForm$',
        views.GetForm,
        name='GetForm'),
    url(r'^postreflection$', views.PostReflection, name='PostReflection'),
    url(r'^listref/(?P<parent_type>\w{3})/(?P<parent_id>\d+)/(?P<list_ref_type>\w{3})$',
        views.list_of_reflections,
        name='list_ref'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/register/$',
        user_manage.Create_User.as_view(form_class=Create_CYL_UserForm),
        name='registration_register'),
    url(r'^info/change/done$', views.info_change_done, name="InfoChangeDone"),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
