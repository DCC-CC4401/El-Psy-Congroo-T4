from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from main import views

urlpatterns = [

    url(r'^$', views.index.as_view(), name='index'),
    url(r'^login/$', views.Login.as_view(),name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup/$', views.SignUp.as_view(),name='signup'),
    url(r'^vendedor/(?P<vendedor>.+)$', views.vendedorprofilepage, name='vendedorprofilepage'),
    url(r'^editar_perfil$', views.EditarPerfil.as_view(), name='editar_perfil'),
    url(r'^agregar_producto$', views.AgregarProducto.as_view(), name='agregar_producto'),
    url(r'^editar_producto/(?P<pid>[0-9]+)/$', views.EditarProducto.as_view(), name='editar_producto'),
    url(r'^eliminar_producto/(?P<pid>[0-9]+)/$', views.productos_delete, name='eliminar_producto'),
    # url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    # url(r'^ajax/dashboard/$', views.get_data, name='data'),
    #url(r'^productos/(?P<vendedor>.+)/delete/(?P<nombre>.+)$', views.productos_delete, name='eliminar_producto'),
    # ajax request to change vendedor active status
    url(r'^ajax/change_active/$', views.change_active, name='change_active'),
    url(r'^ajax/getStock/$', views.getStock, name='getStock'),
    url(r'^ajax/crearTransaccion/$', views.crearTransaccion, name='crearTransaccion'),
    # ajax request to add fav to user
    url(r'^ajax/add_favorite/$', views.add_favorite, name='add_favorite'),
    url(r'^ajax/alerta_policial/$', views.alerta_policial, name='alerta_policial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
