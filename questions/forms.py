from django import forms
from django.contrib.auth import login as authuser
from django.contrib.auth import authenticate

class SettingsForm(forms.Form):

    login = forms.CharField(label='Логин:',max_length=120,required=True,
                            widget=forms.TextInput(attrs={'class':'mdl-textfield__input',
                                                          'type':'text',
                                                          'id':'login_field'}))
    email = forms.EmailField(label='Email',max_length=120,required=True,
                            widget=forms.TextInput(attrs={'class':'mdl-textfield__input',
                                                          'type':'text',
                                                          'id':'email_field'}))
    nickname = forms.CharField(label='Ник:', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class':'mdl-textfield__input',
                                                          'type':'text',
                                                          'id':'nickname_field'}))
    def save_settings(self,user,data):
        user.email = data['email']
        user.username = data['login']
        user.profile.nickname = data['nickname']
        user.profile.save()
        user.save()

class LoginForm(forms.Form):
    login = forms.CharField(label='Логин', max_length=120,required=True,
                            widget=forms.TextInput(attrs={'class':'mdl-textfield__input',
                                                          'type':'text',
                                                          'id':'login_field'}))
    password = forms.CharField(label='Пароль', max_length=120, required=True,
                               widget=forms.TextInput(attrs={'class':'mdl-textfield__input',
                                                             'type':'password',
                                                             'id':'password_field'}))
