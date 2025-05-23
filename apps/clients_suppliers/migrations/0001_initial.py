# Generated by Django 5.2.1 on 2025-05-11 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome Empresa')),
                ('legal_name', models.CharField(max_length=255, verbose_name='Razão Social')),
                ('type', models.CharField(choices=[('C', 'Cliente'), ('S', 'Fornecedor')], max_length=1, verbose_name='Tipo')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('cnpj', models.CharField(max_length=14, unique=True, verbose_name='CNPJ')),
                ('address', models.CharField(max_length=512, verbose_name='Endereço')),
                ('state', models.CharField(max_length=2, verbose_name='Estado')),
                ('city', models.CharField(max_length=255, verbose_name='Cidade')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Telefone')),
                ('billing_email', models.EmailField(max_length=255, verbose_name='Email de Cobrança')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Parte',
                'verbose_name_plural': 'Partes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Telefone')),
                ('position', models.CharField(max_length=255, verbose_name='Cargo')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='clients_suppliers.party', verbose_name='Parte')),
            ],
        ),
    ]
