import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from cx_Oracle import DatabaseError as cxerr
from .models import Profile, check_tel, only_int, Posts, Image
from .dbtest import conndb


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
def admintools(request):
    return render(request, 'admintools.html')

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

def get_profile_praxio(request):
    try:
        conn = conndb()
        cur = conn.cursor()
        # BUSCA FUNCIONARIOS
        cur.execute(
            """
                SELECT DISTINCT
                       FF.CODINTFUNC, 
                       FF.NOMEFUNC NOME,
                       VW.DESCSECAO,
                       VW.DESCFUNCAO,
                       FF.CODIGOFL,
                       CASE
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '1'  THEN 'SPO'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '2'  THEN 'REC'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '3'  THEN 'SSA'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '4'  THEN 'FOR'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '5'  THEN 'MCZ'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '6'  THEN 'NAT'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '7'  THEN 'JPA'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '8'  THEN 'AJU'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '9'  THEN 'VDC'
                           WHEN FF.CODIGOEMPRESA = '1' AND FF.CODIGOFL = '10' THEN 'MG'
                           WHEN FF.CODIGOEMPRESA = '2' AND FF.CODIGOFL = '1'  THEN 'CTG'
                           WHEN FF.CODIGOEMPRESA = '2' AND FF.CODIGOFL = '2'  THEN 'TCO'
                           WHEN FF.CODIGOEMPRESA = '2' AND FF.CODIGOFL = '3'  THEN 'UDI'
                           WHEN FF.CODIGOEMPRESA = '2' AND FF.CODIGOFL = '4'  THEN 'TMA'
                           WHEN FF.CODIGOEMPRESA = '2' AND FF.CODIGOFL = '5'  THEN 'VIX' 
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '30' THEN 'BMA'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '31' THEN 'BPE'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '32' THEN 'BEL'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '33' THEN 'BPB'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '34' THEN 'SLZ'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '35' THEN 'BAL'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '36' THEN 'THE'
                           WHEN FF.CODIGOEMPRESA = '3' AND FF.CODIGOFL = '37' THEN 'BGM'
                           WHEN FF.CODIGOEMPRESA = '4' AND FF.CODIGOFL = '40' THEN 'FMA'
                       END FILIAL,
                       CC.USUARIO,
                       FF.CODIGOUF,
                       TO_CHAR(FF.DTNASCTOFUNC,'YYYY-MM-DD') NASCIMENTO,
                       TO_CHAR(FF.DTADMFUNC,'YYYY-MM-DD') ADMISSAO
                FROM 
                       FLP_FUNCIONARIOS FF,
                       CTR_CADASTRODEUSUARIOS CC,
                       VW_FUNCIONARIOS VW
                WHERE
                       FF.CODINTFUNC = VW.CODINTFUNC                   AND
                       FF.CODINTFUNC = CC.CODINTFUNC                   AND
                   
                       FF.SITUACAOFUNC = 'A'                           AND
                       
                       FF.CODIGOEMPRESA IN (1,2,3,4)
            """)
        res = dictfetchall(cur)
        cur.close()
    except cxerr as err:
        raise err
    else:
        for q in res:
            try:
                Profile.objects.get(codintfunc=q['CODINTFUNC'], username=q['USUARIO'], nomefunc=q['NOME'])
            except ObjectDoesNotExist as err:
                Profile.objects.create(
                    codintfunc=q['CODINTFUNC'],
                    uf=q['CODIGOUF'],
                    dt_admfunc=q['ADMISSAO'],
                    dt_nascfunc=q['NASCIMENTO'],
                    nomefunc=q['NOME'],
                    username=q['USUARIO'],
                    filial=q['FILIAL'],
                    descsecao=q['DESCSECAO'],
                    descfuncao=q['DESCFUNCAO']
                )
            except Exception as e:
                print('Erro:%s, error_type: %s' %(e, type(e)))
            break
        messages.success(request, 'Profiles atualizadas com sucesso!')
        return redirect('base:admintools')

def syncuser(request):
    if request.method == 'POST':
        user = request.user
        opass = request.POST.get('old_password')
        pass1 = request.POST.get('new_password1')
        pass2 = request.POST.get('new_password2')
        if pass1 == pass2:
            npass = Profile.objects.get(username=user)
            if opass == npass.password:
                npass.password = pass1
                npass.save()
    return HttpResponse('200')

def dictfetchall(cursor):
    #Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def testconn(request):
    try:
        conn = conndb()
    except Exception as e:
        return HttpResponse('erro')
    else:
        return HttpResponse('sucesso')

