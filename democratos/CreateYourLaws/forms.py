# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from captcha.fields import CaptchaField
from datetime import date, timedelta
from django.forms import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from registration.forms import RegistrationFormUniqueEmail
from CreateYourLaws.models import (
    Explaination, Proposition, LawProp, Posopinion,
    Negopinion, Question, CYL_user,
)
from ckeditor.widgets import CKEditorWidget


# #################################  User  ####################################


def yesterday():
    yesterday = (date.today() - timedelta(1))
    return yesterday


class Create_CYL_UserForm(RegistrationFormUniqueEmail):
    captcha = CaptchaField()
    date_of_birth = forms.DateField(widget=SelectDateWidget(
                                    years=range(int(date.today().year),
                                                int(date.today().year - 150),
                                                -1)
                                    )
                                    )

    class Meta(UserCreationForm.Meta):
        model = CYL_user
        fields = ('username',
                  'last_name',
                  'first_name',
                  'date_of_birth',
                  'email',
                  'password1',
                  'password2',
                  'captcha',)

        labels = {
            'username': ("Choisissez votre nom d'utilisateur"),
            'last_name': ("Nom:"),
            'first_name': ("Prénom:"),
            'date_of_birth': ("Date de naissance"),

        }
        help_texts = {
            'username': ('Champs requis. max: 30 caractères.' +
                         ' Caractères Alphanumériques et' +
                         ' @/./+/-/_  seulement'),
        }
        error_messages = {
            'username': {
                'max_length': ("Ce nom d'utilisateur est trop long" +
                               " (max 30 charactères)."),
            },
        }
        widget = {
            'date_of_birth': ('DateInput'),
        }

    def __init__(self, *args, **kwargs):
        super(Create_CYL_UserForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Date de naissance:'
        self.fields['email'].label = 'adresse e-mail'
        self.fields['password1'].label = 'Choisissez votre mot de passe'
        self.fields['password2'].label = 'Confirmez votre mot de passe'
        self.fields['password2'].help_text = ("Entrez le même mot de passe " +
                                              "que l'étape précédente pour " +
                                              "vérification")
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['date_of_birth'].required = True

    def is_valid(self):
        # run the parent validation first
        valid = super(Create_CYL_UserForm, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid
        return True


class Info_Change_Form(forms.Form):
    """ Form used to update user's informations """
    NewUserName = forms.CharField(max_length=30, label="nom d'utilisateur")
    NewUserFirstName = forms.CharField(max_length=30, label="Prénom")
    NewUserFamillyName = forms.CharField(max_length=30, label="nom de famille")
    NewEmail = forms.EmailField(label="email")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Info_Change_Form, self).__init__(*args, **kwargs)
        self.fields['NewUserName'].initial = user.username
        self.fields['NewUserFirstName'].initial = user.first_name
        self.fields['NewUserFamillyName'].initial = user.last_name
        self.fields['NewEmail'].initial = user.email

    def save(self, commit=True):
        self.user.username = self.cleaned_data["NewUserName"]
        self.user.first_name = self.cleaned_data["NewUserFirstName"]
        self.user.last_name = self.cleaned_data["NewUserFamillyName"]
        self.user.email = self.cleaned_data["NewEmail"]
        self.user.save()
        return self.user


class Del_account_form(forms.Form):
    password = forms.CharField(label="Entrez votre de passe pour confirmer",
                               widget=forms.PasswordInput)

    def is_valid(self, user):
        # run the parent validation first
        valid = super(Del_account_form, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid
        # verify the passwords match
        if not user.check_password(self.cleaned_data['password']):
            self.add_error("password", 'Le mot de passe est erroné')
            return False
        # all good
        return True


# ############################# Interaction  ##################################
# class CustomFormForReflection(forms.ModelForm):


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'text_q')
        labels = {'title': ('En quelques mots... :'),
                  'text_q': ("Développez votre question")}
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'text_q': CKEditorWidget()
        }


class ExplainationForm(forms.ModelForm):
    class Meta:
        model = Explaination
        fields = ('title', 'text_exp')
        labels = {'title': ("Titre (Décrivez votre idée en quelques mots):"),
                  'text_exp': ('Développez votre commentaire')}
        widgets = {
            'title': forms.TextInput(attrs={'size': 140}),
            'text_exp': CKEditorWidget()
        }

    def clean(self):
        cleaned_data = super(ExplainationForm, self).clean()
        title = cleaned_data.get("title")
        text_exp = cleaned_data.get("text_exp")
        if title == "" and len(text_exp) > 300:
            self.add_error('title',
                           'Titre nécessaire car votre commentaire est long')
        return cleaned_data


class PosopinionForm(forms.ModelForm):
    class Meta:
        model = Posopinion
        fields = ('title', 'text_opp')
        labels = {'title': ('En quelques mots...'),
                  'text_opp': ("Votre opinion:"),
                  }
        widgets = {
            'text_opp': CKEditorWidget()
        }


class NegopinionForm(forms.ModelForm):
    class Meta:
        model = Negopinion
        fields = ('title', 'text_opn')
        labels = {'title': ('En quelques mots...'),
                  'text_opn': ("Votre opinion:"),
                  }
        widgets = {
            'text_opn': CKEditorWidget()
        }


class PropositionForm(forms.ModelForm):
    class Meta:
        model = Proposition
        fields = ('title', 'text_prp', 'details_prp')
        labels = {'title': ('Nommez votre proposition de loi'),
                  'text_prp': ("votre proposition de loi"),
                  'details_prp': ("But recherché par " + \
                                  "cette contre-proposition:"),
                  }
        widgets = {
            'text_prp': CKEditorWidget(config_name='redac_law'),
            'details_prp': CKEditorWidget(config_name='redac_law'),
        }


class CreateNewLawForm(forms.ModelForm):
    class Meta:
        model = LawProp
        fields = ('title', 'text_law', 'details_lwp')
        labels = {'title': ('Ennoncez votre loi'),
                  'text_law': ("votre proposition de loi"),
                  'details_lwp': ("But recherché par " + \
                                  "cette nouvelle loi:"),
                  }
        widgets = {
            'text_law': CKEditorWidget(config_name='redac_law'),
            'details_lwp': CKEditorWidget(config_name='redac_law'),
        }
