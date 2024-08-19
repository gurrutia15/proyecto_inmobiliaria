from app_inmobiliaria.models import Comuna, Inmueble, UserProfile
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

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

def editar_inmueble(inmueble_id:int, nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, cantidad_estacionamientos:int, cantidad_habitaciones:int, cantidad_baños:int, direccion:str, precio_arriendo:int, tipo_inmueble:str, comuna:str, rut_propietario:str, imagen:object):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(cod=comuna)
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
    inmueble.imagen = imagen
    inmueble.save()
    return True

def crear_user(username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, tipo:str='arrendatario', telefono:str=None) -> bool:
    if password != pass_confirm:
        # messages.error(request, 'Las contraseñas no coinciden')
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
        # messages.error(request, 'El rut ya está ingresado')
        return False
    UserProfile.objects.create(
        direccion=direccion,
        telefono=telefono,
        tipo = tipo,
        user=user
    )
    # messages.success(request, 'Usuario creado con éxito! Por favor, ingrese')
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