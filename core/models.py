from django.conf import settings
from django.db import models


class Billetera(models.Model):
    ACTIVA = 'activa'
    INACTIVA = 'inactiva'

    ESTADOS = [
        (ACTIVA, 'Activa'),
        (INACTIVA, 'Inactiva'),
    ]

    idBilletera = models.BigAutoField(primary_key=True)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVA)
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    def depositar(self, monto):
        self.saldo += monto
        self.save(update_fields=['saldo'])
        return Movimiento.registrar(self, Movimiento.DEPOSITO, monto)

    def retirar(self, monto):
        if monto > self.saldo:
            raise ValueError('Saldo insuficiente')
        self.saldo -= monto
        self.save(update_fields=['saldo'])
        return Movimiento.registrar(self, Movimiento.RETIRO, monto)

    def consultarSaldo(self):
        return self.saldo

    def editar(self, **datos):
        for campo, valor in datos.items():
            if hasattr(self, campo):
                setattr(self, campo, valor)
        self.save()
        return self

    def eliminar(self):
        self.delete()

    def __str__(self):
        return f'Billetera #{self.idBilletera} - {self.usuario.username}'


class Movimiento(models.Model):
    DEPOSITO = 'deposito'
    RETIRO = 'retiro'

    TIPOS = [
        (DEPOSITO, 'Deposito'),
        (RETIRO, 'Retiro'),
    ]

    billetera = models.ForeignKey(Billetera, null=True, blank=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    @classmethod
    def registrar(cls, billetera, tipo, monto):
        return cls.objects.create(billetera=billetera, tipo=tipo, monto=monto)

    @classmethod
    def consultar(cls, idMovimiento):
        return cls.objects.get(id=idMovimiento)

    @property
    def idMovimiento(self):
        return self.id

    def __str__(self):
        return f'{self.get_tipo_display()} - ${self.monto}'

class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numeroControl = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
