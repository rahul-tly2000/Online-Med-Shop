from logging import PlaceHolder
from django import forms
from .models import User, Login, Medicine

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=30 , label='First Name')
    last_name = forms.CharField(required=True, max_length=30 , label='Last Name')
    phone_number = forms.CharField(max_length=11, label='Phone Number')
    username = forms.CharField(max_length=30, label='Username')
    email = forms.EmailField(required=True, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    CHOICE = (('User', 'User'), ('Employee', 'Employee'),)
    choose = forms.ChoiceField(choices=CHOICE)
    is_employee = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_user = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_approved = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'phone_number', 'age', 'email', 'password', 'confirm_password')



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Login
        fields='__all__'


class MedicineForm(forms.ModelForm):
    class Meta:
        model=Medicine
        exclude = ('income','requested_stock', 'verify_stock', 'sell')