from django import forms

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

    login = forms.CharField(label='Логин', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'type': 'text',
                                                          'id': 'login_input'}))

    email = forms.CharField(label='Email', max_length=120, required=True,
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

    avatar = forms.FileField(label='Файл', max_length=120, required=True,
                            widget=forms.TextInput(attrs={'class': 'mdl-textfield__input',
                                                          'id': 'file_field'}))