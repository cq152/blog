# -*- coding: utf_8 -*-
from django import forms


class PostAdminForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
