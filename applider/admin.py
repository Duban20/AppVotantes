from django.contrib import admin

from applider.models import Lider

class LiderAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono')
    list_filter = ('status',)
    search_fields = ('nombre', 'cedula')
    ordering = ('nombre',)

    fieldsets = (
        ('Información del Líder', {
            'fields': ('nombre', 'cedula', 'telefono')
        }),
    )

admin.site.register(Lider, LiderAdmin)
