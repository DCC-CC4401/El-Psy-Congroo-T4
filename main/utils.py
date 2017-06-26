import datetime

from main.models import *


def crear_usuario(tipo, form):
    user = User.objects.create_user(username=form.cleaned_data['nombre'],
                                    password=form.cleaned_data['contrasena'], email=form.cleaned_data['email'])
    usuario = Usuario(usuario=user, nombre=form.cleaned_data['nombre'], tipo=tipo)
    usuario.save()
    if tipo == "3":  # ambulante)
        usuarioAmbulante = Vendedor(usuario=usuario, nombre=form.cleaned_data['nombre'])
        usuarioAmbulante.save()
        usuarioAmbulante.formasDePago = form.cleaned_data['pagos']

    if tipo == "2":  # fijo
        usuarioFijo = Vendedor(usuario=usuario, nombre=form.cleaned_data['nombre'],
                               horarioIni=form.cleaned_data['hora_inicio'],
                               horarioFin=form.cleaned_data['hora_fin'],
                               lat=form.cleaned_data['latitud'], long=form.cleaned_data['longitud'])
        usuarioFijo.save()
        usuarioFijo.formasDePago = form.cleaned_data['pagos']


def editar_usuario(user, form):
    avatar = form.cleaned_data['avatar']
    nombre = form.cleaned_data['nombre']
    user.email = form.cleaned_data['email']
    user.username = nombre
    user.save()
    usuario = Usuario.objects.get(usuario=user)
    usuario.nombre = nombre
    if usuario.tipo == 1:
        if avatar is not None:
            usuario.avatar = avatar
        usuario.save()
    else:  # usuario vendedor
        usuario.save()
        usuario = Usuario.objects.get(usuario=user)
        vendedor = Vendedor.objects.get(usuario=usuario)
        vendedor.nombre = nombre
        vendedor.formasDePago = form.cleaned_data['pagos']
        if avatar is not None:
            vendedor.avatar = avatar
        if usuario.tipo == 2:
            vendedor.horarioIni = form.cleaned_data['hora_inicio']
            vendedor.horarioFin = form.cleaned_data['hora_fin']
            vendedor.lat = form.cleaned_data['latitud']
            vendedor.long = form.cleaned_data['longitud']
        vendedor.save()


def agregar_producto(vendedor, form):
    producto = Comida(nombre=form.cleaned_data['nombre'], stock=form.cleaned_data['stock'],
                      categorias=form.cleaned_data['categorias'],
                      descripcion=form.cleaned_data['descripcion'],
                      precio=form.cleaned_data['precio'],
                      imagen=form.cleaned_data['imagen'],
                      vendedor=vendedor)
    producto.save()


def editar_producto(producto_inicial, form):
    producto = Comida.objects.all().filter(nombre=producto_inicial).first()
    producto.nombre = form.cleaned_data['nombre']
    producto.stock = form.cleaned_data['stock']
    producto.categorias = form.cleaned_data['categorias']
    producto.descripcion = form.cleaned_data['descripcion']
    producto.precio = form.cleaned_data['precio']
    if form.cleaned_data['imagen'] is not None:
        producto.imagen = form.cleaned_data['imagen']
    producto.save()


def getVendedores(filtros=[]):
    vendedores = Vendedor.objects.all()
    vendedorList = []
    if filtros:
        for v in vendedores:
            for filtro in filtros:
                if chequear_filtro(v, filtro):
                    if v.usuario.tipo == 2:
                        actualizar_actividad(v)
                    if v.activo and tiene_stock(v):
                        vendedorList.append(v)
    else:
        for v in vendedores:
            if v.usuario.tipo == 2:
                actualizar_actividad(v)
            if v.activo and tiene_stock(v):
                vendedorList.append(v)
    return vendedorList


def getVendedoresFavoritos(user, vendedores):
    favoritos = Favoritos.objects.filter(usuario=user)
    favoritosList = []
    for f in favoritos:
        if f.vendedor in vendedores:
            favoritosList.append(f.vendedor)
    return favoritosList


def actualizar_actividad(vendedor):
    now = datetime.datetime.now().time()
    if vendedor.horarioIni < now < vendedor.horarioFin:
        vendedor.activo = True
        vendedor.save()


def chequear_filtro(vendedor, filtro):
    for item in vendedor.vendedor_respectivo.all():
        if str(filtro) == str(item.categorias):
            return True
    return False


def tiene_stock(v):
    for item in v.vendedor_respectivo.all():
        if item.stock > 0:
            return True
    return False