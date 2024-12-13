from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', views.logout_usuario, name='logout'),  # Ruta para cerrar sesión
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('contacto/', views.contacto, name='contacto'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('categorias/', views.ofertas, name='categorias'),
    path('carrito/', views.contacto, name='carrito'),

    #(No tocar)path('logout/', LogoutView.as_view(), name='logout'),  # URL de logout falta implemetar bien esto

]
