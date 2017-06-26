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
                               horarioFin=form.cleaned_data['hora_fin'])
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
    producto_inicial.nombre = form.cleaned_data['nombre']
    producto_inicial.stock = form.cleaned_data['stock']
    producto_inicial.categorias = form.cleaned_data['categorias']
    producto_inicial.descripcion = form.cleaned_data['descripcion']
    producto_inicial.precio = form.cleaned_data['precio']
    producto_inicial.imagen = form.cleaned_data['imagen']
    producto_inicial.save()


def getVendedores():
    vendedores = Vendedor.objects.all()
    vendedorList = []

    for v in vendedores:
        vendedorList.append(v)
    return vendedorList
