from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import MovimientoForm, RegistroForm, EditarUsuarioForm, EditarPerfilForm
from .models import Billetera, Movimiento, Perfil

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            Perfil.objects.create(
                usuario=user,
                numeroControl=form.cleaned_data['numeroControl']
            )
            Billetera.objects.create(usuario=user)
            auth_login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

@login_required(login_url='login')
def index(request):
    billetera, _ = Billetera.objects.get_or_create(usuario=request.user)
    movimientos = Movimiento.objects.filter(billetera=billetera)
    saldo = billetera.consultarSaldo()
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['monto']
            tipo = request.POST.get('tipo')
            if tipo == Movimiento.RETIRO and monto > saldo:
                messages.error(request, 'No tienes saldo suficiente para retirar esa cantidad.')
            elif tipo == Movimiento.DEPOSITO:
                billetera.depositar(monto)
                messages.success(request, 'Movimiento guardado correctamente.')
            elif tipo == Movimiento.RETIRO:
                billetera.retirar(monto)
                messages.success(request, 'Movimiento guardado correctamente.')
            return redirect('index')
    else:
        form = MovimientoForm()
    return render(request, 'core/index.html', {
        'form': form,
        'saldo': saldo,
        'billetera': billetera,
        'movimientos': movimientos[:5],
    })

@login_required(login_url='login')
def historial_view(request):
    billetera, _ = Billetera.objects.get_or_create(usuario=request.user)
    movimientos = Movimiento.objects.filter(billetera=billetera)
    return render(request, 'core/historial.html', {
        'movimientos': movimientos,
        'billetera': billetera,
    })

@login_required(login_url='login')
def perfil_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user, defaults={'numeroControl': ''})
    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST, instance=request.user)
        perfil_form = EditarPerfilForm(request.POST, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        user_form = EditarUsuarioForm(instance=request.user)
        perfil_form = EditarPerfilForm(instance=perfil)
    return render(request, 'core/perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'perfil': perfil,
    })

@login_required(login_url='login')
def eliminar_usuario_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Cuenta eliminada correctamente.')
        return redirect('login')
    return render(request, 'core/eliminar_usuario.html')

@login_required(login_url='login')
def eliminar_billetera(request):
    if request.method == 'POST':
        Billetera.objects.filter(usuario=request.user).delete()
        Billetera.objects.create(usuario=request.user)
        messages.success(request, 'Billetera eliminada. Se creó una billetera nueva.')
    return redirect('index')