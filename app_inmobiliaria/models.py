from django.db import models
from django.contrib.auth.models import User

# lo que nos piden

# nombres, apellidos, rut, direccion, telefono, correo electronico, tipo

# User (username, email, first_name, last_name, password, ....)


class UserProfile(models.Model):
    tipos=(('arrendador', 'arrendador'),
            ('arrendatario', 'arrendatario'),
            )
    direccion=models.CharField(max_length=255)
    telefono=models.CharField(max_length=12)
    tipo=models.CharField(max_length=20, choices=tipos)
    user=models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    #  (direccion, telefono, tipo, rut):

class Region(models.Model):
    nombre=models.CharField(max_length=100)

class Comuna(models.Model):
    nombre=models.CharField(max_length=100)
    region=models.ForeignKey(Region, related_name='comunas', on_delete=models.CASCADE)