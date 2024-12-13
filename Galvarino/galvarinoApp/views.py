from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistroClienteForm, LoginForm
from django.shortcuts import render
from .forms import ContactoForm
def index(request):
    return render(request, 'index.html')
def carrito(request):
    return render(request, 'carrito.html')



def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})





def quienes_somos(request):
    return render(request, 'quienes_somos.html')

from django.shortcuts import render
from .forms import ContactoForm

def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            # Aquí puedes agregar la lógica para enviar un correo o guardar los datos
            return render(request, 'contacto_exito.html')  # Renderiza una página de éxito
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})
from django.contrib import messages
from django.shortcuts import render
from .forms import ContactForm  # Asegúrate de importar el formulario correspondiente


from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Guarda el mensaje en la base de datos
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact_message.save()

            # Muestra un mensaje de éxito
            messages.success(request, "Gracias por tu mensaje. Nos pondremos en contacto contigo pronto.")
            return render(request, 'contacto.html', {'form': form})
        else:
            # Si el formulario no es válido, muestra los errores
            messages.error(request, "Hubo un error en el formulario. Por favor, revisa los campos.")
    else:
        form = ContactForm()

    return render(request, 'contacto.html', {'form': form})


def ofertas(request):
    return render(request, 'ofertas.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegistroClienteForm

# Vista para iniciar sesión
def login_cliente(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Obtener las credenciales del formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Autenticar al usuario
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Iniciar sesión si las credenciales son correctas
                login(request, user)
                request.session['usuario_id'] = user.id  # Guardar el ID de usuario en la sesión
                messages.success(request, "¡Sesión iniciada correctamente!")
                return redirect('index')  # Redirige a la página principal
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# Vista para registrar un nuevo cliente (si es necesario)
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroClienteForm

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            # Guardamos el cliente y el usuario
            form.save()
            
            messages.success(request, '¡Te has registrado correctamente! Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige a la vista de login
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = RegistroClienteForm()

    return render(request, 'registro_cliente.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_usuario(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, 'Has cerrado tu sesión.')  # Agrega un mensaje de éxito

    return redirect('index')  # Redirige a la página de inicio después de cerrar sesión


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['is_user'] = True  # Establecer 'is_user' a True cuando el usuario inicie sesión
            return redirect('index')
        else:
            return render(request, "login.html", {"error": "Credenciales incorrectas"})
    return render(request, "login.html")

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    if 'is_user' in request.session:
        del request.session['is_user']  # Eliminar la clave is_user de la sesión
    return redirect('index')