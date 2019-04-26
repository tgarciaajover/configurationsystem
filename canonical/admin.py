from django.contrib import admin
from django.forms import ModelForm
from canonical.models import ActivityRegister, Compania, Planta, Sede, RazonParada, Maquina, GrupoMaquina
from django.contrib.auth.decorators import login_required
from setup.models import GraphType, Chart, Dashboard
# Register your models here.

class ActivityRegisterForm(ModelForm):
    class Meta:
        model = ActivityRegister
        fields = ['id_compania', 'id_sede', 'id_planta', 'id_grupo_maquina', 'id_maquina', 'ano', 'mes', 'tipo_actividad', 'id_razon_parada', 'id_produccion']

    def __init__(self, *args, **kwargs):
        super(ActivityRegisterForm, self).__init__(*args, **kwargs)

class ActivityRegisterAdmin(admin.ModelAdmin):
    form = ActivityRegisterForm

    def get_form(self, request, obj=None, **kwargs):
        for key in request.session.keys():
            print('key:' + key + ' value:' + request.session.get(key))
        print('asd')
        form = super(ActivityRegisterAdmin, self).get_form(request, obj=obj, **kwargs)
        return form

    pass

admin.site.register(ActivityRegister, ActivityRegisterAdmin)
admin.site.register(Planta)
admin.site.register(Sede)
admin.site.register(RazonParada)
admin.site.register(Compania)
admin.site.register(Maquina)
admin.site.register(GrupoMaquina)
admin.site.register(GraphType)
admin.site.register(Dashboard)
admin.site.register(Chart)
