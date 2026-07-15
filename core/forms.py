from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class MovimientoForm(forms.Form):
    monto = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'placeholder': '0.00',
            'step': '0.01',
            'min': '1',
        }),
    )

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Nombre')
    last_name = forms.CharField(max_length=50, label='Apellido')
    email = forms.EmailField(label='Correo')
    numeroControl = forms.CharField(max_length=20, label='Número de control')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'numeroControl', 'password1', 'password2']

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
        }

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['numeroControl']
        labels = {'numeroControl': 'Número de control'}