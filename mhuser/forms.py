from django import forms
from django.forms import widgets
from .widgets import XDSoftDateTimePickerInput


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




class DateForm(forms.Form):
    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput()
    )
    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput()
    )