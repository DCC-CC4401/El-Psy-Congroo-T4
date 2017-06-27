from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from main import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^login/$', views.login,name='login'),
    #url(r'^signup/$', views.signup,name='signup'),
    #url(r'^loginReq/',views.loginReq, name = 'loginReq'),
   # url(r'^gestionproductos/$', views.gestionproductos,name='gestionproductos'),
    #url(r'^vendedorprofilepage/$', views.vendedorprofilepage,name='vendedorprofilepage'),
    #url(r'^formView/', views.formView, name='formView'),
    #url(r'^logout/', views.logout, name='logout'),
    #url(r'^register/', views.register, name='register'),
    #url(r'^loggedin/', views.loggedin, name='loggedin'),
    #url(r'^productoReq/', views.productoReq, name='productoReq'),
    #url(r'^vistaVendedorPorAlumno/', views.vistaVendedorPorAlumno, name='vistaVendedorPorAlumno'),
    url(r'^cambiarEstado/$', views.cambiarEstado,name='cambiarEstado'),
    #url(r'^editarVendedor/$', views.editarVendedor,name='editarVendedor'),
    #url(r'^editarDatos/$', views.editarDatos,name='editarDatos'),
    #url(r'^inicioAlumno/', views.inicioAlumno, name='inicioAlumno'),
    url(r'^borrarUsuario/', views.borrarUsuario, name='borrarUsuario'),
    #url(r'^borrarProducto/', views.borrarProducto, name='borrarProducto'),
    #url(r'^editarProducto/', views.editarProducto, name='editarProducto'),
    #url(r'^cambiarFavorito/', views.cambiarFavorito, name='cambiarFavorito'),
   # url(r'^vistaVendedorPorAlumnoSinLogin/', views.vistaVendedorPorAlumnoSinLogin, name='vistaVendedorPorAlumnoSinLogin'),
    #url(r'^editarPerfilAlumno/', views.editarPerfilAlumno,name='editarPerfilAlumno'),
    #url(r'^procesarPerfilAlumno/', views.procesarPerfilAlumno,name='procesarPerfilAlumno'),
    #url(r'^editarUsuario/', views.editarUsuario, name='editarUsuario'),
    url(r'^agregarAvatar/', views.agregarAvatar, name='agregarAvatar'),
    url(r'^signupAdmin/$', views.signupAdmin,name='signupAdmin'),
    url(r'^registerAdmin/$', views.registerAdmin,name='registerAdmin'),
    url(r'^getStock/$', views.getStock,name='getStock'),
    url(r'^verificarEmail/$', views.verificarEmail,name='verificarEmail'),
    url(r'^adminEdit/$', views.adminEdit,name='adminEdit'),
    url(r'^editarUsuarioAdmin/$', views.editarUsuarioAdmin,name='editarUsuarioAdmin'),
    url(r'^loginAdmin/$', views.loginAdmin, name='loginAdmin'),
    url(r'^createTransaction/$', views.createTransaction, name='createTransaction'),
    url(r'^fijoDashboard/$', views.fijoDashboard, name='fijoDashboard'),
    url(r'^ambulanteDashboard/$', views.ambulanteDashboard, name='ambulanteDashboard'),

    #--------------------------- Refactoring ----------------------------#
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^login/$', views.Login.as_view(),name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup/$', views.SignUp.as_view(),name='signup'),
    url(r'^vendedor/(?P<vendedor>.+)$', views.vendedorprofilepage, name='vendedorprofilepage'),
    url(r'^editar_perfil$', views.EditarPerfil.as_view(), name='editar_perfil'),
    url(r'^agregar_producto$', views.AgregarProducto.as_view(), name='agregar_producto'),
    url(r'^editar_producto/(?P<pid>[0-9]+)/$', views.EditarProducto.as_view(), name='editar_producto'),
    url(r'^eliminar_producto/(?P<pid>[0-9]+)/$', views.productos_delete, name='eliminar_producto'),
    #url(r'^productos/(?P<vendedor>.+)/delete/(?P<nombre>.+)$', views.productos_delete, name='eliminar_producto'),
    # ajax request to change vendedor active status
    url(r'^ajax/change_active/$', views.change_active, name='change_active'),
    # ajax request to add fav to user
    url(r'^ajax/add_favorite/$', views.add_favorite, name='add_favorite'),
    url(r'^ajax/alerta_policial/$', views.alerta_policial, name='alerta_policial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
