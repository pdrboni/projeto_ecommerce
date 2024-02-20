from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from . import models
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import copy
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict


# Create your views here.

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil,
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None
                )
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.contexto)


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        

        # usuario logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username
            keys_to_exclude = ['password', 'password2']
            filtered_dict = {key: value for key, value in self.userform.cleaned_data.items() if key not in keys_to_exclude}
            
        
            if password:
                if not check_password(password, usuario.password):
                    messages.success(self.request, 'Senha alterada com sucesso!')
                    usuario.set_password(password)

            elif model_to_dict(models.User.objects.get(id=self.request.user.pk), exclude='id' 'password' 'password2' 'last_login' 'is_superuser' 'groups' 'user_permissions' 'is_staff' 'date_joined' 'is_active') != filtered_dict:
                usuario.email = email
                usuario.first_name = first_name
                usuario.last_name = last_name
                messages.success(self.request, 'Dados alterados com sucesso!')
                usuario.save()

            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                messages.success(self.request, 'Perfil criado com sucesso!')
                perfil.save()
            elif model_to_dict(models.Perfil.objects.get(usuario_id=self.request.user.pk), exclude='id' 'usuario') != self.perfilform.cleaned_data:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                messages.success(self.request, 'Perfil atualizado com sucesso!')
                perfil.save()

        # usuario novo
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
            messages.success(self.request, 'Usuário cadastrado com sucesso!')

        if password:
            autentica = authenticate(self.request, username=usuario, password=password)

            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        
        return redirect('produto:carrinho')

class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')

class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if not username or not password:
            messages.error(self.request, 'Usuário ou senha inválidos')
            return redirect('perfil:criar')
        
        usuario = authenticate(
            self.request, username=username, password=password
        )

        if not usuario:
            messages.error(self.request, 'Usuário ou senha inválidos')
            return redirect('perfil:criar')

        
        login(self.request, user=usuario)
        messages.success(self.request, 'Você fez login e pode concluir sua compra!')

        return redirect('produto:carrinho')

class Logout(View):
    def get(self, *args, **kwargs):
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        logout(self.request)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        return redirect('produto:lista')