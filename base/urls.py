from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/', views.perfil_usuario, name='perfil_usuario')
]
