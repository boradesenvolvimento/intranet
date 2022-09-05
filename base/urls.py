from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/<user>/', views.perfil_usuario, name='perfil_usuario'),
    path('edit_profile/<user>', views.self_profile, name='self_profile')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
