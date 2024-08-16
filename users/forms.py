from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # By default, it is required=True

    class Meta:
        model = User  # Specify the model which interacts with the form
        fields = ['username', 'email', 'password1', 'password2']  # The fields that will be displayed







'''
What is class Meta?
Gives us the nested namespace for configurations and keeps the configurations in one place.
Within the configuration, the model that will be affected will be 'User' model.
'''
