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