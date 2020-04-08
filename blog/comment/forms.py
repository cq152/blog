# -*- coding: utf_8 -*-
import mistune
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    # nickname = forms.CharField(
    #     max_length=50,
    #     label='昵称',
    #     widget=forms.widgets.Input(
    #         attrs={'class': 'form-control', 'style': 'width: 60%;'}
    #     )
    # )
    # email = forms.EmailField(
    #     label='邮箱',
    #     widget=forms.widgets.Input(
    #         attrs={'class': 'form-control', 'style': 'width: 60%;'}
    #     )
    # )
    # site = forms.URLField(
    #     label='网站',
    #     widget=forms.widgets.Input(
    #         attrs={'class': 'form-control', 'style': 'width: 60%;'}
    #     )
    # )
    content = forms.CharField(
        max_length=500,
        label='评论内容（内容不得少于十个字符）',
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'cols': 60}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度过短，请补充！')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['content', ]
