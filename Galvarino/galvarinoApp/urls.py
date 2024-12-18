from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', views.logout_usuario, name='logout'),  # Ruta para cerrar sesión
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('contacto/', views.contacto, name='contacto'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('categorias/', views.ofertas, name='categorias'),
    path('carrito/', views.contacto, name='carrito'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('productos/', views.producto_lista, name='productos'),
    path('productos/', views.producto_lista, name='producto_lista'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    #(No tocar)path('logout/', LogoutView.as_view(), name='logout'),  # URL de logout falta implemetar bien esto

]
