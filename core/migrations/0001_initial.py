# Generated by Django 5.2.3 on 2025-07-01 06:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Planos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planos', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusClinete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, help_text='Status do usuário', max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Finaceiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsavel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, help_text='codigo para compartilhar', max_length=12)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ponts', models.IntegerField(blank=True, default=0, help_text='Pontos acumulados pelo usuário', null=True)),
                ('whatsapp', models.CharField(blank=True, help_text='Número de WhatsApp do usuário', max_length=15, null=True)),
                ('lead_origin', models.IntegerField(blank=True, default=1, help_text='Lead de Origin', null=True)),
                ('objservacao', models.CharField(blank=True, help_text='Observações', max_length=125, null=True)),
                ('unit_id', models.IntegerField(blank=True, default=1, help_text='Unidade Id', null=True)),
                ('plano', models.ForeignKey(blank=True, help_text='Status do usuário', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.planos')),
                ('recomended_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, help_text='Status do usuário', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.statusclinete')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='Vendedora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_notified', models.DateTimeField(default=django.utils.timezone.now, help_text='Última vez que a vendedora foi notificada')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vendedora',
                'verbose_name_plural': 'Vendedoras',
            },
        ),
    ]
