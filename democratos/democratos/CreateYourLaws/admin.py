# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from CreateYourLaws.models import CYL_user, Proposition
from django import forms
from ckeditor.fields import RichTextFormField


class MyUserChangeForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["user_name"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = CYL_user


class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None,
         {'fields': ('date_of_birth',)}),
    )


class PropositionAdminForm(forms.ModelForm):

    class Meta:
        model = Proposition
        exclude = ()


class PropositionAdmin(admin.ModelAdmin):
    form = PropositionAdminForm


admin.site.register(Proposition, PropositionAdmin)
admin.site.register(CYL_user, MyUserAdmin)
