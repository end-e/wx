# -*- coding: utf-8 -*-
from django import forms


class BoundForm(forms.Form):
    username = forms.CharField(required=True)
    telphone = forms.CharField(required=True, max_length=11)
    idnumber = forms.CharField(required=True)
