from django.contrib import admin

from .models import Billetera, Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('idMovimiento', 'billetera', 'tipo', 'monto', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('billetera__usuario__username',)


@admin.register(Billetera)
class BilleteraAdmin(admin.ModelAdmin):
    list_display = ('idBilletera', 'usuario', 'saldo', 'estado', 'fechaCreacion')
    list_filter = ('estado', 'fechaCreacion')
    search_fields = ('usuario__username',)
