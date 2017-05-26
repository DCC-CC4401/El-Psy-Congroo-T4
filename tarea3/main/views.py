from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import LoginForm
from .forms import GestionProductosForm
from .models import Usuario
from .models import Comida
from django.http import HttpResponse
import simplejson


# Create your views here.
def index(request):
    return formView(request)

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
    horarioIni = 0
    horarioFin = 0
    encontrado = False
    email = request.POST.get("email")
    avatar = ''
    password = request.POST.get("password")
    MyLoginForm = LoginForm(request.POST)
    if MyLoginForm.is_valid():
        vendedores = []
        for p in Usuario.objects.raw('SELECT * FROM usuario'):
            if p.contraseña == password and p.email == email:
                tipo = p.tipo
                nombre = p.nombre
                if (tipo == 0):
                    url = 'main/baseAdmin.html'
                    id = p.id
                    tipo = p.tipo
                    encontrado = True
                    break
                elif (tipo == 1):
                    url = 'main/baseAlumno.html'
                    id = p.id
                    avatar = p.avatar
                    tipo = p.tipo
                    encontrado = True
                    break
                elif (tipo == 2):
                    url = 'main/vendedor-fijo.html'
                    id = p.id
                    tipo = p.tipo
                    encontrado = True
                    horarioIni = p.horarioIni
                    horarioFin = p.horarioFin
                    avatar = p.avatar
                    break
                elif (tipo == 3):
                    url = 'main/vendedor-ambulante.html'
                    id = p.id
                    tipo = p.tipo
                    encontrado = True
                    avatar = p.avatar
                    break
        for p in Usuario.objects.raw('SELECT * FROM usuario'):
            if p.tipo == 2 or p.tipo == 3:
                vendedores.append(p.id)
        if encontrado==False:
            return render(request, 'main/login.html', {"error": "Usuario o contraseña invalidos"})
        request.session['id'] = id
        request.session['tipo'] = tipo
        request.session['email'] = email
        vendedoresJson = simplejson.dumps(vendedores)
        return render(request, url, {"email": email, "tipo": tipo, "id": id,"vendedores": vendedoresJson, "nombre": nombre, "horarioIni": horarioIni, "horarioFin" : horarioFin, "avatar" : avatar})
    else:
        return render(request, 'main/login.html', {"error" : "Usuario o contraseña invalidos"})



def gestionproductos(request):
    return render(request, 'main/gestion-productos.html', {})

def vendedorprofilepage(request):
    return render(request, 'main/vendedor-profile-page.html', {})

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
          url = 'main/vendedor-fijo.html'
      elif (tipo == 3):
          url = 'main/vendedor-ambulante.html'
      return render(request, url, {"email" : email, "tipo" : tipo, "id": id})
   else:
      return render(request, 'main/base.html', {})

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
    password = request.POST.get("password")
    horaInicial = request.POST.get("horaIni")
    horaFinal = request.POST.get("horaFin")
    avatar = request.FILES.get("avatar")
    print(avatar)
    formasDePago =[]
    if not (request.POST.get("formaDePago0") is None):
        formasDePago.append(request.POST.get("formaDePago0"))
    if not (request.POST.get("formaDePago1") is None):
        formasDePago.append(request.POST.get("formaDePago1"))
    if not (request.POST.get("formaDePago2") is None):
        formasDePago.append(request.POST.get("formaDePago2"))
    if not (request.POST.get("formaDePago3") is None):
        formasDePago.append(request.POST.get("formaDePago3"))
    usuarioNuevo = Usuario(nombre=nombre,email=email,tipo=tipo,contraseña=password,avatar=avatar,formasDePago=formasDePago,horarioIni=horaInicial,horarioFin=horaFinal)
    usuarioNuevo.save()
    return loginReq(request)

def productoReq(request):
    if request.method == "POST":
        Formulario = GestionProductosForm(request.POST)
        if Formulario.is_valid():
            producto = Comida()
            producto.nombre = request.POST.get("nombre")
            producto.imagen = request.FILES.get("comida")
            producto.precio = request.POST.get("precio")
            producto.stock = request.POST.get("stock")
            producto.descripcion = request.POST.get("descripcion")
            producto.categorias = request.POST.get("categoria")
            producto.save()
        else:
            return render(request, 'main/gestion-productos.html', {"respuesta": "¡Ingrese todos los datos!"})
    return render(request, 'main/vendedor-profile-page.html', {})

def vistaVendedorPorAlumno(request):
    if request.method == 'POST':
        id = int(request.POST.get("id"))
        for p in Usuario.objects.raw('SELECT * FROM usuario'):
            if p.id == id:
                tipo = p.tipo
                nombre = p.nombre
                if tipo == 3:
                    return render(request,'main/vendedor-ambulante-vistaAlumno.html',{"nombre": nombre})
                if tipo == 2:
                    return render(request, 'main/vendedor-fijo-vistaAlumno.html', {"nombre": nombre})