from django import forms
from django.contrib.auth.models import User
from .models import ClientePersonalizado

# Formulario de Login
class LoginForm(forms.Form):
    username = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# Formulario de Registro de Cliente
class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}))

    class Meta:
        model = ClientePersonalizado
        fields = ['rut', 'nombre', 'apellido', 'correo_electronico', 'telefono', 'direccion']
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': '12.345.678-0'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'correo_electronico': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+569 12345678'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Tu dirección'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        # Creamos el usuario
        user = User.objects.create_user(
            username=self.cleaned_data['correo_electronico'],  
            password=self.cleaned_data['password']
        )
        
        # Guardamos el cliente y asociamos el usuario
        cliente = super().save(commit=False)
        cliente.user = user  # Asociamos el cliente al usuario
        if commit:
            cliente.save()
        return cliente

# Formulario de Contacto
class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'id': 'nombre',
            'placeholder': 'Tu nombre completo',
            'required': True
        })
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'id': 'email',
            'placeholder': 'Tu correo electrónico',
            'required': True
        })
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'id': 'mensaje',
            'rows': 5,
            'placeholder': 'Escribe tu mensaje aquí...',
            'required': True
        })
    )

# Formulario de Contacto (alternativo)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'tuemail@ejemplo.com'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí...'}), label='Mensaje')
