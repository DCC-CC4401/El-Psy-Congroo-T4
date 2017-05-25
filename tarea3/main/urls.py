from django.conf.urls import url
from main import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login,name='login'),
    url(r'^signup/$', views.signup,name='signup'),
    url(r'^loginReq/',views.loginReq, name = 'loginReq'),
    url(r'^gestionproductos/$', views.gestionproductos,name='gestionproductos'),
    url(r'^vendedorprofilepage/$', views.vendedorprofilepage,name='vendedorprofilepage'),
]
