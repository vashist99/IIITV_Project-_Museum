from django import forms
from django.contrib.auth.models import User
from App.models import Project

class ProjectForm(forms.ModelForm):
    """Provides form for Project model"""

    class Meta:
        model = Project
        fields = '__all__'


class LoginForm(forms.Form):
    """Provides form for User model"""

    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(forms.ModelForm):
    """Provides form for User model"""
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm_password',
                                       widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']