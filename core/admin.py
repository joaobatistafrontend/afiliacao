from django.contrib import admin
from .models import *

admin.site.site_header = 'Painel de Administração'
admin.site.site_title = 'Administração do Indicador'
admin.site.register(StatusClinete)
admin.site.register(Planos)
admin.site.register(UserProfile)
admin.site.register(Vendedora)
admin.site.register(Finaceiro)
