from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()
    
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1',
                  'password2')
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.CharField()
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email',)
