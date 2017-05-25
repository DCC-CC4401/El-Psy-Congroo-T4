from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'main/base.html', {})

def login(request):
    return render(request, 'main/login.html', {})

def signup(request):
    return render(request, 'main/signup.html', {})

def gestionproductos(request):
    return render(request, 'main/gestion-productos.html', {})

def vendedorprofilepage(request):
    return render(request, 'main/vendedor-profile-page.html', {})