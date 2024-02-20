from django import forms
from django.contrib.auth.models import User
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario', )

class UserForm(forms.ModelForm):
    
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Caso esteja logado e não queira atualizar sua senha, poderá deixá-la em branco.'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação da senha',
        help_text='Caso esteja logado e não queira atualizar sua senha, poderá deixá-la em branco.'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = data['username']

        if usuario_data == 'AnonymousUser':
            password_data = data['password3']
            password2_data = data['password4']
        else:
            password_data = data['password']
            password2_data = data['password2']
        email_data = data['email']

        # poderia fazer também da seguinte forma:
        # usuario_data = cleaned.get('username')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'Email já existe'
        error_password_needing = 'Senha obrigatória'
        error_non_match_password = 'Senhas não conferem'
        error_short_password = 'A senha deve conter pelo menos 6 caracteres'


        # Usuários logados: atualização
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_non_match_password
                    validation_error_msgs['password2'] = error_non_match_password

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_short_password

        # Usuários não logados: cadastro
        else:
            
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_password_needing

            if not password2_data:
                validation_error_msgs['password2'] = error_password_needing

            if password_data != password2_data:
                validation_error_msgs['password'] = error_non_match_password
                validation_error_msgs['password2'] = error_non_match_password

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_short_password

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))