# Generated by Django 5.2.3 on 2025-07-01 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusclinete',
            name='status',
            field=models.CharField(blank=True, help_text='Status do usuário', max_length=60, null=True),
        ),
    ]
