from django.contrib import admin

from dashboard.models import Dashboard, Chart

# Register your models here.

# Registro del modelo Dashboard en el modulo de administrador.
admin.site.register(Dashboard)
# Registro del modelo Chart en el modulo de administrador.
admin.site.register(Chart)