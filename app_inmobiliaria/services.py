from app_inmobiliaria.models import Comuna, Inmueble, UserProfile
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db import connection
from django.contrib import messages

def crear_inmueble(nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, cantidad_estacionamientos:int, cantidad_habitaciones:int, cantidad_baños:int, direccion:str, precio_arriendo:int, tipo_inmueble:str, comuna_id:str, rut_propietario:str):
    comuna = Comuna.objects.get(id=comuna_id)
    propietario = User.objects.get(username=rut_propietario)
    Inmueble.objects.create(
        nombre = nombre,
        descripcion = descripcion,
        m2_construidos = m2_construidos,
        m2_totales = m2_totales,
        cantidad_estacionamientos = cantidad_estacionamientos,
        cantidad_habitaciones = cantidad_habitaciones,
        cantidad_baños = cantidad_baños,
        direccion = direccion,
        precio_arriendo = precio_arriendo,
        tipo_inmueble = tipo_inmueble,
        comuna = comuna,
        propietario = propietario,
    )
    return True

def editar_inmueble(inmueble_id:int, nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, cantidad_estacionamientos:int, cantidad_habitaciones:int, cantidad_baños:int, direccion:str, precio_arriendo:int, tipo_inmueble:str, comuna:str, rut_propietario:str):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(id=comuna)
    propietario = User.objects.get(username=rut_propietario)
    inmueble.nombre = nombre
    inmueble.descripcion = descripcion
    inmueble.m2_construidos = m2_construidos
    inmueble.m2_totales = m2_totales
    inmueble.cantidad_estacionamientos = cantidad_estacionamientos
    inmueble.cantidad_habitaciones = cantidad_habitaciones
    inmueble.cantidad_baños = cantidad_baños
    inmueble.direccion = direccion
    inmueble.precio_arriendo = precio_arriendo
    inmueble.tipo_inmueble = tipo_inmueble
    inmueble.comuna = comuna
    inmueble.propietario = propietario
    inmueble.save()
    return True

def crear_user(request, username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, tipo:str='arrendatario', telefono:str=None) -> bool:
    if password != pass_confirm:
        messages.error(request, 'Las contraseñas no coinciden')
        return False
    try:
        user = User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name,
        )
    except IntegrityError:
        messages.error(request, 'El rut ya está ingresado')
        return False
    UserProfile.objects.create(
        direccion=direccion,
        telefono=telefono,
        tipo = tipo,
        user=user
    )
    messages.success(request, 'Usuario creado con éxito! Por favor, ingrese')
    return True

def eliminar_inmueble(inmueble_id):
    Inmueble.objects.get(id=inmueble_id).delete()
    return True

def eliminar_user(rut:str):
    eliminar = User.objects.get(username=rut)
    eliminar.delete()
    return True

def editar_user_sin_password(rut:str, first_name:str, last_name:str, email:str, direccion:str, tipo:str, telefono:str=None):
    user = User.objects.get(username=rut)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono = telefono
    user_profile.tipo = tipo
    user_profile.save()

def cambio_password(request, password:str, password_repeat:str):
    if password != password_repeat:
        messages.warning(request, 'Las contraseñas no coinciden')
        return False
    request.user.set_password(password)
    request.user.save()
    messages.success(request, 'Contraseña actualizada con éxito')
    return True

def obtener_propiedades_comunas(filtro):
    if filtro is None:
        return Inmueble.objects.all().order_by('comuna')
    
    return Inmueble.objects.filter(Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro)).order_by('comuna')

def obtener_propiedades_regiones(filtro):
    consulta = '''
    select I.nombre, I.descripcion, R.nombre as region from app_inmobiliaria_inmueble as I
    join app_inmobiliaria_comuna as C on I.comuna_id = C.id
    join app_inmobiliaria_region as R on C.region_id = R.id
    order by R.id;
    '''
    if filtro is not None:
        filtro = filtro.lower()
        consulta = f'''
        select I.nombre, I.descripcion, R.nombre as region from app_inmobiliaria_inmueble as I
        join app_inmobiliaria_comuna as C on I.comuna_id = C.id
        join app_inmobiliaria_region as R on C.region_id = R.id where lower(I.nombre) like '%{filtro}%' or lower(I.descripcion) like '%{filtro}%'
        order by R.id;
        '''
    cursor = connection.cursor()
    cursor.execute(consulta)
    registros = cursor.fetchall() # LAZY LOADING
    return registros