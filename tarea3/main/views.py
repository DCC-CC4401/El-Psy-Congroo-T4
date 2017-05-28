from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import LoginForm
from .forms import GestionProductosForm
from .forms import editarProductosForm
from .models import Usuario
from .models import Comida
from .models import Favoritos
import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from multiselectfield import MultiSelectField
from django.core.files.storage import default_storage
# Create your views here.
def index(request):
    vendedores = []
    # lista de vendedores
    for p in Usuario.objects.raw('SELECT * FROM usuario'):
        if p.tipo == 2 or p.tipo == 3:
            vendedores.append(p.id)
    vendedoresJson = simplejson.dumps(vendedores)
    return render(request, 'main/baseAlumno-sinLogin.html', {"vendedores": vendedoresJson})

def login(request):
    return render(request, 'main/login.html', {})

def signup(request):
    return render(request, 'main/signup.html', {})

def loggedin(request):
    return render(request, 'main/loggedin.html', {})


def loginReq(request):

    #inicaliar variables
    tipo = 0
    url = ''
    id = 0
    horarioIni = 0
    horarioFin = 0
    encontrado = False
    email = request.POST.get("email")
    avatar = ''
    password = request.POST.get("password")
    listaDeProductos = []
    formasDePago = []
    activo = False

    #buscar vendedor en base de datos
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
                    avatar = p.avatar
                    break
                elif (tipo == 2):
                    url = 'main/vendedor-fijo.html'
                    id = p.id
                    tipo = p.tipo
                    encontrado = True
                    horarioIni = p.horarioIni
                    horarioFin = p.horarioFin
                    request.session['horarioIni'] = horarioIni
                    request.session['horarioFin'] = horarioFin
                    avatar = p.avatar
                    activo = p.activo
                    formasDePago = p.formasDePago
                    request.session['formasDePago'] = formasDePago
                    break
                elif (tipo == 3):
                    url = 'main/vendedor-ambulante.html'
                    id = p.id
                    tipo = p.tipo
                    encontrado = True
                    avatar = p.avatar
                    activo = p.activo
                    formasDePago = p.formasDePago
                    request.session['formasDePago'] = formasDePago
                    break

        #si no se encuentra el usuario, se retorna a pagina de login
        if encontrado==False:
            return render(request, 'main/login.html', {"error": "Usuario o contraseña invalidos"})

        #crear datos de sesion
        request.session['id'] = id
        request.session['tipo'] = tipo
        request.session['email'] = email
        request.session['nombre'] = nombre
        request.session['avatar'] = str(avatar)
        # si son vendedores, crear lista de productos
        for p in Usuario.objects.raw('SELECT * FROM usuario'):
            if p.tipo == 2 or p.tipo == 3:
                vendedores.append(p.id)
        vendedoresJson = simplejson.dumps(vendedores)

        #obtener alimentos en caso de que sea vendedor fijo o ambulante
        if tipo == 2 or tipo == 3:
            i = 0
            for producto in Comida.objects.raw('SELECT * FROM comida WHERE idVendedor = "' + str(id) +'"'):
                listaDeProductos.append([])
                listaDeProductos[i].append(producto.nombre)
                categoria = str(producto.categorias)
                listaDeProductos[i].append(categoria)
                listaDeProductos[i].append(producto.stock)
                listaDeProductos[i].append(producto.precio)
                listaDeProductos[i].append(producto.descripcion)
                listaDeProductos[i].append(str(producto.imagen))
                i += 1
        listaDeProductos = simplejson.dumps(listaDeProductos,ensure_ascii=False).encode('utf8')

        #limpiar argumentos de salida segun tipo de vista
        argumentos ={"email": email, "tipo": tipo, "id": id,"vendedores": vendedoresJson, "nombre": nombre, "horarioIni": horarioIni, "horarioFin" : horarioFin, "avatar" : avatar, "listaDeProductos" : listaDeProductos}
        if (tipo == 0):
            argumentos = {"nombre": nombre,"id": id,}
        if (tipo == 1):
            argumentos = {"nombre": nombre,  "tipo": tipo, "id": id,"vendedores": vendedoresJson, "avatarSesion": avatar}
        if (tipo == 2):
            argumentos = {"nombre": nombre,  "tipo": tipo, "id": id,"horarioIni": horarioIni, "horarioFin" : horarioFin, "avatar" : avatar, "listaDeProductos" : listaDeProductos, "activo" : activo, "formasDePago" : formasDePago}
        if (tipo ==3):
            argumentos ={"nombre": nombre,  "tipo": tipo, "id": id,"avatar" : avatar, "listaDeProductos" : listaDeProductos, "activo" : activo, "formasDePago" : formasDePago}

        #enviar a vista respectiva de usuario
        return render(request, url, argumentos)

    #retornar en caso de datos invalidos
    else:
        return render(request, 'main/login.html', {"error" : "Usuario o contraseña invalidos"})



def gestionproductos(request):
    if request.session.has_key('id'):
        email = request.session['email']
        tipo = request.session['tipo']
        id = request.session['id']
        if tipo == 3:
            path = "main/baseVAmbulante.html"
        if tipo == 2:
            path = "main/baseVFijo.html"
    return render(request, 'main/agregar-productos.html', {"path" : path})

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
    horarioIni = 0
    horarioFin = 0
    avatar = ""
    if request.method == "POST":
        if request.session.has_key('id'):
            id = request.session['id']
            email = request.session['email']
            tipo = request.session['tipo']
            if tipo == 3:
                path = "main/baseVAmbulante.html"
                url ="main/vendedor-ambulante.html"
            if tipo == 2:
                path = "main/baseVFijo.html"
                url = "main/vendedor-fijo.html"
            Formulario = GestionProductosForm(request.POST)
            if Formulario.is_valid():
                producto = Comida()
                producto.idVendedor = id
                producto.nombre = request.POST.get("nombre")
                producto.imagen = request.FILES.get("comida")
                producto.precio = request.POST.get("precio")
                producto.stock = request.POST.get("stock")
                producto.descripcion = request.POST.get("descripcion")
                producto.categorias = request.POST.get("categoria")
                producto.save()
            else:
                return render(request, 'main/agregar-productos.html', {"path" : path, "respuesta": "¡Ingrese todos los datos!"})

    # obtener alimentos en caso de que sea vendedor fijo o ambulante
    i = 0
    listaDeProductos=[]
    for producto in Comida.objects.raw('SELECT * FROM comida WHERE idVendedor = "' + str(id) + '"'):
        listaDeProductos.append([])
        listaDeProductos[i].append(producto.nombre)
        categoria = str(producto.categorias)
        listaDeProductos[i].append(categoria)
        listaDeProductos[i].append(producto.stock)
        listaDeProductos[i].append(producto.precio)
        listaDeProductos[i].append(producto.descripcion)
        listaDeProductos[i].append(str(producto.imagen))
        i += 1
    listaDeProductos = simplejson.dumps(listaDeProductos, ensure_ascii=False).encode('utf8')

    for p in Usuario.objects.raw('SELECT * FROM usuario'):
        if p.id == id:
            avatar = p.avatar
            horarioIni = p.horarioIni
            horarioFin = p.horarioFin
            nombre = p.nombre
    return render(request, url, {"email": email, "tipo": tipo, "id": id, "nombre": nombre, "horarioIni": horarioIni, "horarioFin" : horarioFin, "avatar" : avatar, "listaDeProductos" : listaDeProductos})

def vistaVendedorPorAlumno(request):
    if request.method == 'POST':
        id = int(request.POST.get("id"))
        for p in Usuario.objects.raw('SELECT * FROM usuario'):
            if p.id == id:
                favorito = 0
                for f in Favoritos.objects.raw('SELECT * FROM Favoritos'):
                    if request.session['id'] == f.idAlumno:
                        if id == f.idVendedor:
                            favorito = 1
                tipo = p.tipo
                nombre = p.nombre
                avatar = p.avatar
                formasDePago = p.formasDePago
                if tipo == 3:
                    url = 'main/vendedor-ambulante-vistaAlumno.html'
                    break
                if tipo == 2:
                    url = 'main/vendedor-fijo-vistaAlumno.html'
                    break
    # obtener alimentos
    i = 0
    listaDeProductos = []
    for producto in Comida.objects.raw('SELECT * FROM comida WHERE idVendedor = "' + str(id) + '"'):
        listaDeProductos.append([])
        listaDeProductos[i].append(producto.nombre)
        categoria = str(producto.categorias)
        listaDeProductos[i].append(categoria)
        listaDeProductos[i].append(producto.stock)
        listaDeProductos[i].append(producto.precio)
        listaDeProductos[i].append(producto.descripcion)
        listaDeProductos[i].append(str(producto.imagen))
        i += 1
    avatarSesion = request.session['avatar']
    listaDeProductos = simplejson.dumps(listaDeProductos, ensure_ascii=False).encode('utf8')
    return render(request, url, {"nombre": nombre, "tipo": tipo, "id": id, "avatar" : avatar, "listaDeProductos" :listaDeProductos,"avatarSesion": avatarSesion,"favorito": favorito, "formasDePago": formasDePago})

def vistaVendedorPorAlumnoSinLogin(request):
    if request.method == 'POST':
        id = int(request.POST.get("id"))
        for p in Usuario.objects.raw('SELECT * FROM usuario'):
            if p.id == id:
                tipo = p.tipo
                nombre = p.nombre
                avatar = p.avatar
                formasDePago = p.formasDePago
                if tipo == 3:
                    url = 'main/vendedor-ambulante-vistaAlumno-sinLogin.html'
                    break
                if tipo == 2:
                    url = 'main/vendedor-fijo-vistaAlumno-sinLogin.html'
                    break
                    # obtener alimentos
    i = 0
    listaDeProductos = []
    for producto in Comida.objects.raw('SELECT * FROM comida WHERE idVendedor = "' + str(id) + '"'):
        listaDeProductos.append([])
        listaDeProductos[i].append(producto.nombre)
        categoria = str(producto.categorias)
        listaDeProductos[i].append(categoria)
        listaDeProductos[i].append(producto.stock)
        listaDeProductos[i].append(producto.precio)
        listaDeProductos[i].append(producto.descripcion)
        listaDeProductos[i].append(str(producto.imagen))
        i += 1
    listaDeProductos = simplejson.dumps(listaDeProductos, ensure_ascii=False).encode('utf8')
    return render(request, url, {"nombre": nombre, "tipo": tipo, "id": id,"avatar" : avatar, "listaDeProductos" :listaDeProductos, "formasDePago": formasDePago})


def cambiarEstado(request):
    if request.method == 'POST':
        id_vendedor = int(request.POST.get("id"))
        estado = bool(request.POST.get("estado"))
        print(estado)
        if estado == False:
            Usuario.objects.get(id=id_vendedor).update(activo=False)
        else:
            Usuario.objects.filter(id=id_vendedor).update(activo=False)
        # Usuario.save()


def editarVendedor(request):
    if request.session.has_key('id'):
        id = request.session['id']
        nombre = request.session['nombre']
        formasDePago = request.session['formasDePago']
        avatar = request.session['avatar']
        tipo = request.session['tipo']
        if (tipo == 2):
            horarioIni = request.session['horarioIni']
            horarioFin = request.session['horarioFin']
            argumentos = {"nombre": nombre, "id": id, "horarioIni": horarioIni, "horarioFin": horarioFin,
                          "avatar": avatar, "formasDePago": formasDePago}
            url = 'main/editar-vendedor-fijo.html'
        elif (tipo == 3):
            argumentos = {"nombre": nombre, "id": id, "avatar": avatar, "formasDePago": formasDePago}
            url = 'main/editar-vendedor-ambulante.html'
        return render(request, url, argumentos)
    else:
        return render(request, 'main/base.html', {})

def editarDatos(request):
    nombre = request.POST.get("nombre")
    tipo = request.POST.get("tipo")
    horaInicial = request.POST.get("horaIni") # TODO poner en un if segun el tipo
    horaFinal = request.POST.get("horaFin")
    avatar = request.FILES.get("avatar")
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

@csrf_exempt
def borrarProducto(request):
    if request.method == 'GET':
        if request.is_ajax():
            comida = request.GET.get('eliminar')
            Comida.objects.filter(nombre=comida).delete()
            data = {"eliminar" : comida}
            return JsonResponse(data)

@csrf_exempt
def editarProducto(request):
    if request.method == 'POST':
        if request.is_ajax():
            form = editarProductosForm(data=request.POST, files=request.FILES)
            print(request.POST)
            print(request.FILES)
            nombreOriginal = request.POST.get("nombreOriginal")
            nuevoNombre = request.POST.get('nombre')
            nuevoPrecio = (request.POST.get('precio'))
            nuevoStock = (request.POST.get('stock'))
            nuevaDescripcion = request.POST.get('descripcion')
            nuevaCategoria = (request.POST.get('categoria'))
            nuevaImagen = request.FILES.get("comida")
            if nuevoNombre != "":
                if Comida.objects.filter(nombre=nuevoNombre).exists():
                    data = {"respuesta": "repetido"}
                    return JsonResponse(data)
                Comida.objects.filter(nombre=nombreOriginal).update(nombre=nuevoNombre)
            if nuevoPrecio != "" :
                   Comida.objects.filter(nombre=nombreOriginal).update(precio=int(nuevoPrecio))
            if nuevoStock != "" :
                   Comida.objects.filter(nombre=nombreOriginal).update(stock=int(nuevoStock))
            if nuevaDescripcion != "":
                   Comida.objects.filter(nombre=nombreOriginal).update(descripcion=nuevaDescripcion)
            if  nuevaCategoria != None:
                   Comida.objects.filter(nombre=nombreOriginal).update(categorias=(nuevaCategoria))
            if nuevaImagen != None:
                filename = nombreOriginal + ".jpg"
                with default_storage.open('../media/productos/' + filename, 'wb+') as destination:
                    for chunk in nuevaImagen.chunks():
                        destination.write(chunk)
                Comida.objects.filter(nombre =nombreOriginal).update(imagen='/productos/'+filename)

            data = {"respuesta" : nombreOriginal}
            return JsonResponse(data)

def cambiarFavorito(request):
    if request.method == "GET":
        if request.is_ajax():
            favorito = request.GET.get('favorito')
            agregar = request.GET.get('agregar')
            if agregar == "si":
                nuevoFavorito = Favoritos()
                nuevoFavorito.idAlumno = request.session['id']
                nuevoFavorito.idVendedor = favorito
                nuevoFavorito.save()
                respuesta = {"respuesta": "si"}
            else:
                Favoritos.objects.filter(idAlumno=request.session['id']).filter(idVendedor=favorito).delete()
                respuesta = {"respuesta": "no"}
            return JsonResponse(respuesta)