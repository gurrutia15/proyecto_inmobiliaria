from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# lo que nos piden

# nombres, apellidos, rut, direccion, telefono, correo electronico, tipo

# User (username, email, first_name, last_name, password, ....)



class UserProfile(models.Model):                # Extender clase usuario
    tipos=(
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),          # Primer campo es con el nombre que se guarda en BD, el segundo el que aparece en pantalla
        
    )
    direccion=models.CharField(max_length=255)
    telefono=models.CharField(max_length=12, null=True)
    tipo=models.CharField(max_length=20, choices=tipos)
    user=models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    #  (direccion, telefono, tipo, rut):
    def __str__(self):
        nombre = self.user.first_name
        apellido = self.user.last_name
        usuario = self.user.username
        tipo = self.tipo
        return f'{nombre} {apellido} | {usuario} | {tipo}'
    
class Region(models.Model):
    nombre=models.CharField(max_length=255)

class Comuna(models.Model):
    nombre=models.CharField(max_length=255)
    region=models.ForeignKey(Region, related_name='comunas', on_delete=models.RESTRICT)

    def __str__(self) -> str:
        nombre=self.nombre
        codigo=self.id
        return f' {nombre} {codigo}'

class Inmueble(models.Model):
    inmuebles=(
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    )
    nombre =  models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    m2_construidos=models.IntegerField(validators=[MinValueValidator(1)])
    m2_totales=models.IntegerField(validators=[MinValueValidator(1)])
    cantidad_estacionamientos = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    cantidad_habitaciones =models.IntegerField(validators=[MinValueValidator(1)], default=1)
    cantidad_baños=models.IntegerField(validators=[MinValueValidator(1)], default=1)
    direccion=models.CharField(max_length=255) 
    precio_arriendo=models.IntegerField(validators=[MinValueValidator(1)], default=1)
    tipo_inmueble=models.CharField(max_length=12, choices=inmuebles)
    comuna=models.ForeignKey(Comuna, related_name='inmuebles', on_delete=models.RESTRICT)     
    propietario=models.ForeignKey(User, related_name='inmueble', on_delete=models.RESTRICT)

    def __str__(self) -> str:
        nombre = self.nombre
        comuna = self.comuna
        tipo = self.tipo_inmueble
        return f'{nombre} {comuna} | {tipo}'