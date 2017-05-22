from django import forms
from .models import User,Profile
from django.contrib.auth.hashers import make_password

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

class CommentForm(forms.Form):

    message = forms.CharField(label='Сообщение',max_length=500,required=True,
                                   widget=forms.TextInput(attrs={'class':'mdl-textfield mdl-js-textfield'}))

class AskForm(forms.Form):

    title = forms.CharField(label='Заголовок', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'text',
                                                          'id': 'title_input'}))

    message = forms.CharField(label='Текст',max_length=500,required=True,
                                   widget=forms.TextInput(attrs={'class':'mdl-textfield mdl-js-textfield'}))

    tags = forms.CharField(label='Теги', max_length=120, required=False,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'text',
                                                          'id': 'tags_input'}))
class RegistrationForm(forms.Form):
    error_css_class = 'error'

    login = forms.CharField(label='Логин', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'text',
                                                          'id': 'login_input'}))

    email = forms.EmailField(label='Email', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'text',
                                                          'id': 'email_input'}))

    nickname = forms.CharField(label='Никнейм', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'text',
                                                          'id': 'nickname_input'}))

    password = forms.CharField(label='Пароль', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'password',
                                                          'id': 'password_input'}))

    repeatpassword = forms.CharField(label='Повторите Пароль', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'password',
                                                          'id': 'repeat_password_input'}))

    avatar = forms.ImageField(label='Файл', max_length=120, required=False)

    def clean(self):
        if User.objects.filter(username = self.cleaned_data['login']).count() != 0:
            raise forms.ValidationError("User with this login already exists")
        if self.cleaned_data['password'] != self.cleaned_data['repeatpassword']:
            raise forms.ValidationError("Passwords don't match!")

    def register(self):
        profile = Profile(
            username=self.cleaned_data['login'],
            nickname=self.cleaned_data['nickname'],
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password']),
            avatar=self.cleaned_data['avatar']
        )
        profile.save()