from django.forms import ModelForm, HiddenInput
from django import forms
from blog.models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField


class BlogForm(forms.Form):
    essay = CKEditorWidget()
    label = forms.TextInput()

