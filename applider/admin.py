from django.contrib import admin

from applider.models import Lider

class LiderAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono', 'status')
    list_filter = ('status',)
    search_fields = ('nombre', 'cedula')
    ordering = ('nombre',)

    fieldsets = (
        ('Información del Líder', {
            'fields': ('nombre', 'cedula', 'telefono')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
    )

admin.site.register(Lider, LiderAdmin)
