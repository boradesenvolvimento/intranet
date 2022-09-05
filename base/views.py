import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Profile, check_tel, only_int


@login_required(login_url='/accounts/login/')
def index_view(request):
    return render(request, 'index.html', {})

@login_required(login_url='/accounts/login/')
def perfil_usuario(request, user):
    usuario = Profile.objects.get(user_ref__username=user)
    return render(request, 'userprofile.html', {'usuario':usuario})

@login_required(login_url='/accounts/login/')
def self_profile(request, user):
    if str(user) == str(request.user):
        usuario = Profile.objects.get(user_ref__username=user)
        if request.method == 'POST':
            form = request.POST
            foto = request.FILES.get('fotoperfil')
            try:
                if form['biograph']:
                    usuario.bio = form['biograph']
                if foto:
                    usuario.foto_perfil = foto
                if form['email']:
                    usuario.email = form['email']
                if form['telefone']:
                    if re.match(r'[0-9]{2}[0-9]{5}[0-9]{4}', form['telefone']):
                        usuario.telefone = form['telefone']
                    else:
                        messages.error(request, 'Telefone inválido, verifique o número digitado')
                        raise ValidationError
                if form['ramal']:
                    try:
                        ramal = int(form['ramal'])
                    except (ValueError, TypeError):
                        messages.error(request, 'Ramal inválido, verifique o número digitado')
                        raise ValidationError
                    else:
                        usuario.ramal = ramal
                if form['filial']:
                   usuario.filial = form['filial']
            except Exception as e:
                raise e
            else:
                usuario.save()
                messages.success(request, 'Atualizado com sucesso!!')
            finally:
                return redirect('base:perfil_usuario', user=usuario)
        return render(request, 'selfprofile.html', {'usuario':usuario})
    else:
        return HttpResponse('erro')
