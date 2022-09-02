from django.shortcuts import render


def index_view(request):
    return render(request, 'index.html', {})

def perfil_usuario(request):
    return render(request, 'profile.html', {})
