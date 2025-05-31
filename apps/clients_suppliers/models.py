from django.db import models
from django.contrib.auth.models import User

class Party(models.Model):
    TYPE_CHOICES = (
        ('C', 'Cliente'),
        ('S', 'Fornecedor'),
    )
    
    name = models.CharField('Nome Empresa', max_length=255)
    legal_name = models.CharField('Razão Social', max_length=255)
    type = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES)
    is_active = models.BooleanField('Ativo', default=True)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True)
    address = models.CharField('Endereço', max_length=512)
    state = models.CharField('Estado', max_length=2)
    city = models.CharField('Cidade', max_length=255)
    phone_number = models.CharField('Telefone', max_length=20)
    billing_email = models.EmailField('Email de Cobrança', max_length=255)
    notes = models.TextField('Observações', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='party')

    class Meta:
        verbose_name = 'Parte'
        verbose_name_plural = 'Partes'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Contact(models.Model):
    party = models.ForeignKey(
        Party,
        on_delete=models.PROTECT,
        related_name='contacts',
        verbose_name='Parte'
    )
    name = models.CharField('Nome', max_length=255)
    email = models.EmailField('Email', max_length=255)
    phone_number = models.CharField('Telefone', max_length=20)
    position = models.CharField('Cargo', max_length=255)

    def __str__(self):
        return f"{self.name} ({self.party.name})"