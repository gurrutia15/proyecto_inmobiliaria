from django.shortcuts import render, redirect
from .services import crear_user, editar_user_sin_password, cambio_password, crear_inmueble
from django.contrib.auth.decorators import login_required
from .models import Inmueble, Region, Comuna
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html',)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        tipo = request.POST['tipo']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
            
        crear = crear_user(request, username, first_name, last_name, email, password, password_repeat, direccion, tipo, telefono)

        if crear: 
            return redirect('/accounts/login') 
        
        return render(request, 'registration/register.html', {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'direccion': direccion,
            'telefono': telefono,
            'tipo': tipo,
            })
    else: 
        return render(request, 'registration/register.html')
    


@login_required
def profile(request):
    id_usuario = request.user.id
    propiedades = Inmueble.objects.filter(propietario_id=id_usuario)
    context = {
        'propiedades': propiedades
    }

    if request.method == 'POST':
        if request.POST['telefono'].strip() != '':
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            tipo = request.POST['tipo']
            editar_user_sin_password(username, first_name, last_name, email, direccion, tipo, telefono)
            messages.success(request, 'Ha actualizado sus datos con exito')
            return redirect('/accounts/profile')
        else:
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            tipo = request.POST['tipo']
                        
            editar_user_sin_password(username, first_name, last_name, email, tipo, direccion)
            messages.success(request, 'Ha actualizado sus datos con exito sin telefono')
            return redirect('/accounts/profile')
    else:
        return render(request, 'profile.html', context)
    
def change_pass(request):
    password= request.POST['password']
    password_repeat= request.POST['password_repeat']
    cambio_password(request, password, password_repeat)
    return redirect('/accounts/profile')

@login_required
def add_propiedad(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all().order_by('nombre')
    tipos_inmuebles = Inmueble.inmuebles
    context = {
        'regiones': regiones,
        'comunas':  comunas,
        'tipos_inmuebles': tipos_inmuebles
    }

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        m2_construidos = int(request.POST ['m2_construidos'])
        m2_totales = int(request.POST ['m2_totales'])
        cantidad_estacionamientos = int(request.POST ['cantidad_estacionamientos'])
        cantidad_habitaciones = int(request.POST ['cantidad_habitaciones'])
        cantidad_baños = int(request.POST ['cantidad_baños'])
        direccion = request.POST ['direccion']
        precio_arriendo = int(request.POST ['precio_arriendo'])
        tipo_inmueble = request.POST ['tipo_inmueble']
        comuna_id = request.POST ['comuna_id']
        rut_propietario = request.user

        crear = crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, cantidad_estacionamientos, cantidad_habitaciones, cantidad_baños, direccion, precio_arriendo, tipo_inmueble, comuna_id, rut_propietario)

        if crear:
            messages.success(request, 'Propiedad ingresada con éxito')
            return redirect('profile')
        messages.warning(request, 'Hubo un problema al crear la propiedad')
        return redirect('add_propiedad', context)
    else:
        return render(request, 'add_propiedad.html', context)