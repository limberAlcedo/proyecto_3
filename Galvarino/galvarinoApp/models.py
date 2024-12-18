from django.db import models
from django.contrib.auth.models import User

class ClientePersonalizado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=20, choices=[
        ('normal', 'Comprador'),
        ('picker', 'Picker'),
        ('administrador', 'Administrador'),
    ], default='normal')
    
    # Agregamos el campo para la clave de usuario
    clave_usuario = models.CharField(max_length=128)  # Almacenar la clave de usuario (de manera no segura)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
# models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mayoreo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Campo para el stock
    codigo_producto = models.CharField(max_length=50, unique=True)  # Campo para el código del producto
    categoria = models.CharField(max_length=50)  # Campo para la categoría del producto
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del producto
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # Fecha de la última actualización del producto

    def __str__(self):
        return self.nombre
