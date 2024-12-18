# Generated by Django 5.1.4 on 2024-12-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galvarinoApp', '0003_clientepersonalizado_clave_usuario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('foto', models.ImageField(upload_to='productos/')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_mayoreo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('codigo_producto', models.CharField(max_length=50, unique=True)),
                ('categoria', models.CharField(max_length=50)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]