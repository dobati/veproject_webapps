# -*- coding: utf-8 -*-
from django import forms
from .models import UserInput
from django.forms import ModelForm, Textarea

# personalised from for user translation

class UserInputForm(forms.Form):
    form_translation = forms.CharField(
        widget=forms.Textarea(attrs={'cols':25, 'rows':4}),
        label='',
        ## currently not working due to structure of views.py
        #required=True,
        #error_messages={'required': 'Please enter a translation or click "See solution"'},
        )
      
    class Meta: 
        model = UserInput