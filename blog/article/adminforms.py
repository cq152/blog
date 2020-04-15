# -*- coding: utf_8 -*-
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from article.models import Post


class PostAdminForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    content = forms.CharField(widget=forms.HiddenInput, required=False)

    content_ck = forms.CharField(widget=CKEditorUploadingWidget, label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea, label='正文', required=False)

    class Meta:
        model = Post
        fields = {
            'category', 'tag', 'summary', 'title', 'is_markdown',
            'content', 'content_md', 'content_ck', 'status'
        }

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_markdown = self.cleaned_data.get('is_markdown')
        if is_markdown:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)

        if not content:
            self.add_error(content_field_name,'必选项')
            return
        self.cleaned_data['content'] = content
        return super(PostAdminForm, self).clean()

    class Media:
        js = ('js/post_editor.js', )

