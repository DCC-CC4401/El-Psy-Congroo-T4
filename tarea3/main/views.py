from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import LoginForm
from .models import Usuario
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'main/base.html', {})

def login(request):
    return render(request, 'main/login.html', {})

def signup(request):
    return render(request, 'main/signup.html', {})

def loggedin(request):
    return render(request, 'main/loggedin.html', {})


def loginReq(request):
    tipo = 0
    url = ''
    id = 0
    email = request.POST.get("email")
    password = request.POST.get("password")
    for p in Usuario.objects.raw('SELECT * FROM usuario'):
        if p.contraseña == password and p.email == email:
            tipo=p.tipo
            if (tipo==0):
                url= 'main/baseAdmin.html'
            elif (tipo == 1):
                url = 'main/baseAlumno.html'
            elif (tipo == 2):
                url = 'main/baseVFijo.html'
            elif (tipo == 3):
                url= 'main/baseVAmbulante.html'
        id = p.id
        tipo = p.tipo
    request.session['id'] = id
    request.session['tipo'] = tipo
    request.session['email'] = email
    return render(request, url, {"email" : email, "tipo" : tipo, "id": id})


def formView(request):
   if request.session.has_key('id'):
      email = request.session['email']
      tipo = request.session['tipo']
      id = request.session['id']
      if (tipo == 0):
          url = 'main/baseAdmin.html'
      elif (tipo == 1):
          url = 'main/baseAlumno.html'
      elif (tipo == 2):
          url = 'main/baseVFijo.html'
      elif (tipo == 3):
          url = 'main/baseVAmbulante.html'
      return render(request, url, {"email" : email, "tipo" : tipo, "id": id})
   else:
      return render(request, 'main/login.html', {})


def gestionproductos(request):
    return render(request, 'main/gestion-productos.html', {})

def vendedorprofilepage(request):
    return render(request, 'main/vendedor-profile-page.html', {})

def logout(request):
   try:
      del request.session['id']
   except:
      pass
   return render(request, 'main/base.html', {})

def register(request):
    tipo = request.POST.get("tipo")
    nombre = request.POST.get("nombre")
    email = request.POST.get("email")
    #group1 = request.POST.get("group1")
    password = request.POST.get("password")
    horaInicial = request.POST.get("horaIni")
    horaFinal = request.POST.get("horaFin")
    formasDePago = request.POST.get("formasDePago[]")
    usuarioNuevo = Usuario(nombre=nombre,email=email,tipo=tipo,contraseña=password,avatar="jpge",formasDePago=formasDePago,horarioIni=horaInicial,horarioFin=horaFinal)
    usuarioNuevo.save()
    return render(request, 'main/loggedin.html', {"email" : email})