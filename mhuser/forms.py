from django import forms
from django.forms import widgets
from ckeditor.fields import RichTextFormField

class Register(forms.Form):
    user_name = forms.CharField()
    user_email = forms.EmailField()
    user_password = forms.CharField()
    user_type = forms.CharField(
        widget=widgets.RadioSelect(choices=[('normal', '普通用户'), ('doctor', '医生')]),
        initial=[1, 2],
    )

class Login(forms.Form):
    user_name = forms.CharField()
    user_password = forms.CharField()

# class SelectForm(forms.Form):
#     DATA_TYPE_CHOICES = (
#         ('pressure', '血压数据'),
#         ('oxygen', '血氧数据'),
#         ('heartbeat', '心跳数据'),
#         ('tem', '体温数据')
#     )
#     charged = forms.ChoiceField(choices=DATA_TYPE_CHOICES)
