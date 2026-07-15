import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, models


def copiar_usuario_auth(apps, schema_editor):
    Billetera = apps.get_model('core', 'Billetera')

    for billetera in Billetera.objects.select_related('usuario__auth_user'):
        if billetera.usuario_id and billetera.usuario.auth_user_id:
            billetera.auth_user_id = billetera.usuario.auth_user_id
            billetera.save(update_fields=['auth_user'])


def crear_usuario_prueba(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Billetera = apps.get_model('core', 'Billetera')

    user, _ = User.objects.get_or_create(
        username='prueba',
        defaults={
            'email': 'prueba@example.com',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    )
    user.password = make_password('prueba123')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()

    Billetera.objects.get_or_create(usuario=user)


def eliminar_usuario_prueba(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='prueba').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_billetera_remove_movimiento_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='billetera',
            name='auth_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(copiar_usuario_auth, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='billetera',
            name='usuario',
        ),
        migrations.RenameField(
            model_name='billetera',
            old_name='auth_user',
            new_name='usuario',
        ),
        migrations.AlterField(
            model_name='billetera',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Registro',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.RunPython(crear_usuario_prueba, eliminar_usuario_prueba),
    ]
