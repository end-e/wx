# -*- coding: utf-8 -*-
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    img = forms.FileField()
    shop_code = forms.CharField()
