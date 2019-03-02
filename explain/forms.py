from django.forms import ModelForm, HiddenInput
from .models import Explain
from ckeditor.widgets import CKEditorWidget
from django import forms
from ckeditor.fields import RichTextFormField

class ExplainForm(forms.Form):
    context = CKEditorWidget()