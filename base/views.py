import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Profile, check_tel, only_int, Posts, Image


@login_required(login_url='/intranet/accounts/login/')
def index_view(request):
    context = {
        'posts': Posts.objects.all().order_by('-pub_date'),
    }
    return render(request, 'index.html', context)

@login_required(login_url='/intranet/accounts/login/')
def perfil_usuario(request, user):
    usuario = Profile.objects.get(user_ref__username=user)
    return render(request, 'userprofile.html', {'usuario':usuario})

@login_required(login_url='/intranet/accounts/login/')
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
                    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                    if re.match(regex, form['email']):
                        usuario.email = form['email']
                    else:
                        messages.error(request, 'Email inválido, gentileza verificar')
                        raise ValidationError
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

@login_required(login_url='/intranet/accounts/login/')
def create_posts(request):
    if request.method == 'POST':
        body = request.POST.get('body')
        img = request.FILES.getlist('imagens')
        if body:
            autor = Profile.objects.get(username=request.user)
            post = Posts.objects.create(text=body, autor=autor)
            if img:
                for q in img:
                    Image.objects.create(file=q, post_ref=post)
            return redirect('base:index')
        print(body, img)
    return render(request, 'createpost.html')

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(nomefunc__icontains=query)
        )
        if query == '' or not profile_list:
            messages.error(request, 'Não encontrado usuário da busca, gentileza verificar.')
            return render(request, 'search.html')
        else:
            context = {
                'profile_list': profile_list
            }
            return render(request, 'search.html', context)
