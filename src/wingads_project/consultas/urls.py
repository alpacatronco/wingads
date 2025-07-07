from django.urls import path
from . import views

app_name = 'consultas' # Define el nombre de la aplicación para evitar conflictos de nombres

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('crear_consulta/', views.crear_consulta, name='crear_consulta'),
    path('iniciar_pago/<int:consulta_id>/', views.iniciar_pago, name='iniciar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('pago_fallido/', views.pago_fallido, name='pago_fallido'),
] 