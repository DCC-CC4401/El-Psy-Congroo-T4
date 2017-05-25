from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import LoginForm
from .forms import GestionProductosForm
from .models import Usuario
from .models import Comida


# Create your views here.
def index(request):
    return render(request, 'main/base.html', {})

def login(request):
    return render(request, 'main/login.html', {})

def signup(request):
    return render(request, 'main/signup.html', {})




def loginReq(request):
    tipo = 0
    email = request.POST.get("email")
    password = request.POST.get("password")
    for p in Usuario.objects.raw('SELECT * FROM usuario'):
        if p.contraseña == password and p.email == email:
            print(p.id)
            tipo=p.tipo
            if (tipo==0):
                return render(request, 'main/baseAdmin.html', {})
            if (tipo == 1):
                return render(request, 'main/baseAlumno.html', {})
            if (tipo == 2):
                return render(request, 'main/baseVFijo.html', {})
            if (tipo == 3):
                return render(request, 'main/baseVAmbulante.html', {})


    #return render(request, 'main/loggedin.html', {"email" : tipo})

def gestionproductos(request):
    return render(request, 'main/gestion-productos.html',{} )

def productoReq(request):

    if request.method == "POST":
        Formulario = GestionProductosForm(request.POST)
        if Formulario.is_valid():
            producto = Comida()
            producto.nombre = request.POST.get("nombre")
            producto.precio = request.POST.get("precio")
            producto.stock = request.POST.get("stock")
            producto.descripcion = request.POST.get("descripcion")
            producto.categorias = request.POST.get("categoria")
            producto.save()
        else:
            return render(request, 'main/gestion-productos.html', {"respuesta":"¡Ingrese todos los datos!"})

    return render(request,'main/vendedor-profile-page.html', {})

def vendedorprofilepage(request):
    return render(request, 'main/vendedor-profile-page.html', {})