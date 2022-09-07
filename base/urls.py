from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('perfil/<user>/', views.perfil_usuario, name='perfil_usuario'),
    path('editar_perfil/<user>', views.self_profile, name='self_profile'),
    path('nova_postagem/', views.create_posts, name='create_posts'),
    path('search/', views.UserSearch.as_view(), name='profile-search'),
    path('ferramentas-adm/', views.admintools, name='admintools'),
    path('get_profile_praxio/', views.get_profile_praxio, name='get_profile_praxio'),
    path('testconn/', views.testconn, name='testconn'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
