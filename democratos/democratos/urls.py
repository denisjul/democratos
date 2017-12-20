"""democratos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url('$', Home.as_view(), name='home')
Including another URLconf
    1. Import the re_path() function: from django.conf.urls import url, re_path
    2. Add a URL to urlpatterns:  url('blog/', re_path('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
import CreateYourLaws

urlpatterns = [
    path('admin/', admin.site.urls),
    path('CYL/', include('CreateYourLaws.urls')),
    # url('ckeditor/', re_path('ckeditor.urls')),
    path('', CreateYourLaws.views.home),
]
