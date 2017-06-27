import simplejson
import pusher
from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.db.models import Count
from django.db.models import Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.utils import *
from .forms import *
from .models import *


def getProductos(vendedor):
    productos = Comida.objects.filter(vendedor=vendedor).all()
    listaProductos = []

    for p in productos:
        listaProductos.append(p)
    return listaProductos


class index(View):
    @staticmethod
    def get(request):
        userDj = request.user
        if not userDj.is_authenticated():
            return render(request, 'refactoring/index.html', {'userDj': userDj, 'vendedores': getVendedores(),
                                                              'form': form_filtros()})
        user = Usuario.objects.get(usuario=userDj)
        vendedores = getVendedores()
        return render(request, 'refactoring/index.html', {'user': user, 'userDj': userDj,
                                                          'vendedores': vendedores,
                                                          'vendedores_favoritos': getVendedoresFavoritos(user, vendedores),
                                                          'form': form_filtros()})

    def post(self, request):
        userDj = request.user
        user = Usuario.objects.get(usuario=userDj)
        form = form_filtros(request.POST)
        if form.is_valid():
            filtros = form.cleaned_data['filtros']
            favoritos = form.cleaned_data['favoritos']
            vendedores = getVendedores(filtros)
            if favoritos:
                vendedores = getVendedoresFavoritos(user, vendedores)
            return render(request, 'refactoring/index.html', {'user': user, 'userDj': userDj,
                                                              'vendedores': vendedores,
                                                              'vendedores_favoritos': getVendedoresFavoritos(user, vendedores),
                                                              'form': form_filtros()})
        vendedores = getVendedores()
        return render(request, 'refactoring/index.html', {'user': user, 'userDj': userDj,
                                                          'vendedores': vendedores,
                                                          'vendedores_favoritos': getVendedoresFavoritos(user, vendedores),
                                                          'form': form_filtros()})


class Login(View):
    @staticmethod
    def get(request):
        form = Formulario_Ingreso()
        return render(request, 'refactoring/login.html', {'form': form})

    def post(self, request):
        form = Formulario_Ingreso(request.POST)
        if not form.is_valid():
            self.get(request)
        email = request.POST['email']
        password = request.POST['password']
        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'refactoring/login.html', {
                'error': 'Usuario o contraseña invalidos', 'form': form, })
        if user.is_active:
            auth.login(request, user)
            usuario = Usuario.objects.get(usuario=user)
            tipo = usuario.tipo
            if tipo == 1:  # alumno
                return redirect('index')
            else:  # vendedor
                return redirect('vendedorprofilepage', vendedor=usuario)
        return render(request, 'refactoring/login.html', {'form': form})


class SignUp(View):
    def get(self, request):
        form = Formulario_Registro()
        return render(request, 'refactoring/signup.html', {'form': form})

    def post(self, request):
        form = Formulario_Registro(request.POST, request.FILES)
        if form.is_valid():
            try:
                tipo = form.cleaned_data['tipo_cuenta']
                crear_usuario(tipo, form)
                return redirect('login')

            except IntegrityError:
                return render(request, 'refactoring/signup.html',
                              {'mensage': 'El usuario ya esta en uso', 'form': form})
            except KeyError as e:
                return render(request, 'refactoring/signup.html', {'message': e.args[0], 'form': form})
        else:
            form = Formulario_Registro()
            return render(request, 'refactoring/signup.html', {'form': form})


def vendedorprofilepage(request, vendedor):
    vendedorUser = Vendedor.objects.get(nombre=vendedor)
    user = request.user
    favorito = False
    metodospago = ''
    favs = 0
    usuario = None
    for m in vendedorUser.formasDePago.all():
        metodospago += m.forma + ' '
    if vendedorUser.usuario.tipo == 2:
        actualizar_actividad(vendedorUser)
    if user.is_authenticated:
        usuario = Usuario.objects.get(usuario=user)
        tipo = usuario.tipo
        if tipo == 1:
            if Favoritos.objects.filter(usuario=usuario, vendedor=vendedorUser).count() != 0:
                favorito = True
        else:
            for fav in Favoritos.objects.all():
                if fav.vendedor == vendedorUser:
                    favs += 1
    data = {
        'userDj': user,
        'user': usuario,
        'vendedor': vendedorUser,
        'vendedor_estado': 'Activo' if vendedorUser.activo else 'Inactivo',
        'vendedor_tipo': 'Vendedor fijo' if vendedorUser.usuario.tipo == 2 else 'Vendedor ambulante',
        'vendedor_metodospago': metodospago,
        'productos': getProductos(vendedorUser),
        'favorito': favorito,
        'vendedor_numero_favs': favs,
    }
    return render(request, 'refactoring/vendedor-profile-page.html', data)


class EditarPerfil(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('index')
        user = request.user
        vendedor = Vendedor.objects.get(usuario=user.usuario)
        inicial = {'nombre': user.username, 'email': user.email}
        if user.usuario.tipo == 1:
            inicial['favoritos'] = Favoritos.objects.filter(usuario=user.usuario)
        else:
            inicial['pagos'] = vendedor.formasDePago.all()
        if user.usuario.tipo == 2:
            inicial['hora_inicio'] = vendedor.horarioIni
            inicial['hora_fin'] = vendedor.horarioFin

        form = Formulario_Actualizar_Perfil(initial=inicial)
        usuario = request.user.usuario
        if request.user.usuario.tipo != 1:
            vendedor = Vendedor.objects.get(usuario=usuario)
            return render(request, 'refactoring/editar-perfil.html', {'form': form, 'userDj': request.user,
                                                                      'user': usuario, 'vendedor': vendedor})
        return render(request, 'refactoring/editar-perfil.html', {'form': form, 'userDj': request.user,
                                                                  'user': usuario})

    def post(self, request):
        form = Formulario_Actualizar_Perfil(request.POST, request.FILES)
        if not request.user.is_authenticated() or not form.is_valid():
            return self.get(request)
        user = User.objects.get(username=request.user)

        if user.check_password(form.cleaned_data['contrasena']):
            editar_usuario(user, form)
            if user.usuario.tipo == 1:
                return redirect('index')
            else:
                vendedor = Vendedor.objects.get(usuario=request.user.usuario)
                return redirect('vendedorprofilepage', vendedor=vendedor)
        return render(request, 'refactoring/editar-perfil.html', {'form': form, 'userDj': request.user, 'user': user})


class AgregarProducto(View):
    def get(self, request):
        form = Formulario_Producto()
        if request.user.usuario.tipo != 1:
            usuario = request.user.usuario
            vendedor = Vendedor.objects.get(usuario=usuario)
            return render(request, 'refactoring/agregar-productos.html', {'form': form, 'userDj': request.user,
                                                                          'user': usuario, 'vendedor': vendedor})
        return render(request, 'refactoring/agregar-productos.html', {'form': form, 'userDj': request.user,
                                                                      'user': Usuario.objects.get(usuario=request.user)})

    def post(self, request):
        form = Formulario_Producto(request.POST, request.FILES)
        if form.is_valid():
            vendedor = Vendedor.objects.get(usuario=request.user.usuario)
            agregar_producto(vendedor, form)
            return redirect('vendedorprofilepage', vendedor=vendedor)
        else:
            form = Formulario_Producto()
            return render(request, 'refactoring/agregar-productos.html', {'form': form, 'userDj': request.user,
                                                                          'user': Usuario.objects.get(usuario=request.user)})


class EditarProducto(View):
    def get(self, request, pid):
        usuario = Usuario.objects.get(usuario=request.user)
        vendedor = Vendedor.objects.get(usuario=usuario)
        productos = Comida.objects.filter(vendedor=vendedor)
        producto_inicial = productos.get(id=pid)
        form = Formulario_Producto(instance=producto_inicial)
        return render(request, 'refactoring/editar-productos.html', {'form': form, 'userDj': request.user,
                                                                     'user': usuario, 'vendedor': vendedor})

    def post(self, request, pid):
        usuario = Usuario.objects.get(usuario=request.user)
        vendedor = Vendedor.objects.get(usuario=usuario)
        productos = Comida.objects.filter(vendedor=vendedor)
        producto_inicial = productos.get(id=pid)
        form = Formulario_Producto(request.POST, request.FILES)
        if form.is_valid():
            editar_producto(producto_inicial, form)
            return redirect('vendedorprofilepage', vendedor=vendedor)
        else:
            form = Formulario_Producto()
            return render(request, 'refactoring/editar-productos.html', {'form': form, 'userDj': request.user,
                                                                         'user': request.user.usuario,
                                                                         'vendedor': vendedor})


def productos_delete(request, pid):
    usuario = Usuario.objects.get(usuario=request.user)
    vendedor = Vendedor.objects.get(usuario=usuario)
    productos = Comida.objects.filter(vendedor=vendedor)
    producto = productos.get(id=pid)
    producto.delete()
    return redirect('vendedorprofilepage', vendedor=vendedor)


def logout(request):
    auth.logout(request)
    return redirect('index')

def getStock(request):
    pid = request.GET.get("id", None)
    vendedor = Vendedor.objects.filter(id=request.GET.get("vendedor", None))
    productos = Comida.objects.filter(vendedor=vendedor)
    producto = productos.get(id=pid)
    stock = producto.stock
    if request.GET.get("op", None) == "suma":
        nuevoStock = stock + 1
        Comida.objects.filter(id=pid).update(stock=nuevoStock)
    if request.GET.get("op", None) == "resta":
        nuevoStock = stock - 1
        if stock == 0:
            return JsonResponse({"stock": stock})
        Comida.objects.filter(id=pid).update(stock=nuevoStock)
    return JsonResponse({"stock": stock})

def crearTransaccion(request):
    pid = request.GET.get("id", None)
    vendedor = Vendedor.objects.get(id=request.GET.get("vendedor", None))
    productos = Comida.objects.filter(vendedor=vendedor)
    producto = productos.get(id=pid)
    fecha_hoy = datetime.datetime.now().replace(microsecond=0).date()
    precio = 0
    if Comida.objects.filter(id=pid).exists():
        precio = producto.precio
        transaccionNueva = Transacciones(vendedor=vendedor, comida=producto, fecha=fecha_hoy, precio=precio)
        transaccionNueva.save()
    else:
        return HttpResponse('error message')
    return HttpResponse("")

# def dashboard(request):
#     usuario = Usuario.objects.get(usuario=request.user)
#     vendedor = Vendedor.objects.get(usuario=usuario)
#     return render(request, 'refactoring/dashboard.html', {'user': usuario, 'userDj': request.user,
#                                                               'vendedor': vendedor})

class Dashboard(View):

    def post(self, request):
        pid = request.POST.get("vendedorId", None)
        usuario = Usuario.objects.get(id=pid)
        vendedor = Vendedor.objects.get(usuario=usuario)
        fecha_hoy = datetime.datetime.now().replace(microsecond=0).date()
        transactiones = Transacciones.objects.filter(vendedor=vendedor)
        transactiones_hoy = transactiones.filter(fecha=fecha_hoy)

        transaccionesDiarias = Transacciones.objects.filter(vendedor=vendedor).values('fecha').annotate(conteo=Count('fecha'))
        temp_transaccionesDiarias = list(transaccionesDiarias)
        transaccionesDiariasArr = []

        for element in temp_transaccionesDiarias:
           aux = []
           aux.append(element['fecha'].strftime('%d-%m-%Y'))
           aux.append(element['conteo'])
           transaccionesDiariasArr.append(aux)
        transaccionesDiariasArr = simplejson.dumps(transaccionesDiariasArr)

        gananciasDiarias = transactiones_hoy.values('fecha').annotate(ganancia=Sum('precio'))
        temp_gananciasDiarias = list(gananciasDiarias)
        gananciasDiariasArr = []
        for element in temp_gananciasDiarias:
            aux = []
            aux.append(element['fecha'].strftime('%d-%m-%Y'))
            aux.append(element['ganancia'])
            gananciasDiariasArr.append(aux)
        gananciasDiariasArr = simplejson.dumps(gananciasDiariasArr)

        #todos los productos del vendedor
        productos = Comida.objects.filter(vendedor=vendedor).values('nombre','precio')
        temp_productos = list(productos)
        productosArr = []
        productosPrecioArr = []
        for element in temp_productos:
            aux = []
            productosArr.append(element['nombre'])
            aux.append(element['nombre'])
            aux.append(element['precio'])
            productosPrecioArr.append(aux)
        productosArr = simplejson.dumps(productosArr)
        productosPrecioArr = simplejson.dumps(productosPrecioArr)
        print(productosPrecioArr)

        #productos vendidos hoy con su cantidad respectiva
        fechaHoy = str(timezone.now()).split(' ', 1)[0]
        productosHoy = Transacciones.objects.filter(vendedor=vendedor,fecha=fechaHoy).values('comida').annotate(conteo=Count('comida'))
        temp_productosHoy = list(productosHoy)
        productosHoyArr = []
        for element in temp_productosHoy:
             aux = []
             aux.append(element['comida'])
             aux.append(element['conteo'])
             productosHoyArr.append(aux)
        productosHoyArr = simplejson.dumps(productosHoyArr)
        print(productosHoyArr)
        return render(request, 'refactoring/dashboard.html', {'user': usuario, 'userDj': request.user,
                                                              'vendedor': vendedor,"transacciones":transaccionesDiariasArr,"ganancias":gananciasDiariasArr,"productos":productosArr,"productosHoy":productosHoyArr,"productosPrecio":productosPrecioArr})

def change_active(request):
    usuario = Usuario.objects.get(usuario=request.user)
    vendedor = Vendedor.objects.get(usuario=usuario)
    lat = request.GET.get('lat', None)
    lng = request.GET.get('long', None)
    if lat is not None and lng is not None:
        vendedor.lat = request.GET.get('lat', None)
        vendedor.long = request.GET.get('long', None)
    vendedor.activo = not vendedor.activo
    vendedor.save()
    return HttpResponse("")

def add_favorite(request):
    user = Usuario.objects.get(nombre=request.user)
    vendedor = Vendedor.objects.get(nombre=request.GET.get('vendedor', None))
    if Favoritos.objects.filter(usuario=user, vendedor=vendedor).count() != 0:
        Favoritos.objects.filter(usuario=user, vendedor=vendedor).delete()
    else:
        nuevoFav = Favoritos(usuario=user, vendedor=vendedor)
        nuevoFav.save()
    vendedor.users.all().count()
    return HttpResponse("")


def alerta_policial(request):
    pusher_client = pusher.Pusher(
        app_id='358730',
        key='43806ba42b9b3916fd09',
        secret='a81c51a9bb4bd6b42287',
        cluster='us2',
        ssl=True
    )
    lat = request.GET.get('lat', None)
    lng = request.GET.get('long', None)
    pusher_client.trigger('canal-alerta', 'evento-alerta', {'message': '¡Cuidado! Hay policías cerca', 'lat': lat, 'lng': lng})
    return HttpResponse("")
