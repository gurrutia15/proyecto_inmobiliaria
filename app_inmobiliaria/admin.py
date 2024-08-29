from django.contrib import admin
from .models import UserProfile, Comuna, Inmueble

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    # list_display = ['direccion', 'tipo', 'user']
    pass

class InmuebleAdmin(admin.ModelAdmin):
    pass

class ComunaAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Inmueble, InmuebleAdmin)