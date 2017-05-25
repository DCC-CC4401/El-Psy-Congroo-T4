from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import LoginForm
from .models import Usuario


# Create your views here.
def index(request):
    return render(request, 'main/base.html', {})

def login(request):
    return render(request, 'main/login.html', {})

def signup(request):
    return render(request, 'main/signup.html', {})

<<<<<<< HEAD


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
=======
def gestionproductos(request):
    return render(request, 'main/gestion-productos.html', {})

def vendedorprofilepage(request):
    return render(request, 'main/vendedor-profile-page.html', {})
>>>>>>> cc4d7ac03fced100649cdc4a315d29a4b3412b3f
