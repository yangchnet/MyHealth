from django.forms import ModelForm, HiddenInput
from .models import BlogComment, BottomComment
from ckeditor.widgets import CKEditorWidget
from django import forms
from ckeditor.fields import RichTextFormField

class BlogCommentForm(ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']
        widgets = {
            'comment': CKEditorWidget
        }

class CKEditorForm(forms.Form):
    content = RichTextFormField()

class BottomCommentForm(ModelForm):
    class Meta:
        model = BottomComment
        fields = ['comment', 'followed_comment', 'followed_self']
        widgets = {
            'followed_comment': CKEditorWidget,
            'followed_self': CKEditorWidget,
        }