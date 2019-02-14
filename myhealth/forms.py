from django import forms
from django.forms import widgets
from ckeditor.fields import RichTextFormField

class Register(forms.Form):
    user_name = forms.CharField()
    user_email = forms.EmailField()
    user_password = forms.CharField()
    user_type = forms.CharField(
        widget=widgets.RadioSelect(choices=[(1, '普通用户'), (2, '医生')]),
        initial=[1, 2],
    )

class Login(forms.Form):
    user_name = forms.CharField()
    user_password = forms.CharField()

class CKEditorForm(forms.Form):
    content = RichTextFormField()