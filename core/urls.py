from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('historial/', views.historial_view, name='historial'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('eliminar-usuario/', views.eliminar_usuario_view, name='eliminar_usuario'),
    path('eliminar-billetera/', views.eliminar_billetera, name='eliminar_billetera'),
]