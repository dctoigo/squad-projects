from django.db import models
from apps.contracts.models import Contract
from apps.manager.models import Technology, BillingType, PaymentInterval

class Project(models.Model):
    code = models.AutoField(primary_key=True)
    title = models.CharField('Title', max_length=255)
    contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL,
        related_name='projects', null=True, blank=True
    )
    client = models.ForeignKey(
        'clients_suppliers.Party',
        on_delete=models.PROTECT,
        related_name='projects',
        null=True, blank=True,
        help_text='Set when no contract.'
    )
    scope = models.TextField('Scope')
    main_contact = models.CharField('Contact Person', max_length=255)

    # billing fields for avulso or override
    billing_type     = models.ForeignKey(
        BillingType, on_delete=models.PROTECT, related_name='+',
        null=True, blank=True
    )
    payment_interval = models.ForeignKey(
        PaymentInterval, on_delete=models.PROTECT, related_name='+',
        null=True, blank=True
    )
    rate_or_value = models.DecimalField(
        'Rate/Value', max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Fill if billing is hourly or fixed.'
    )

    start_date = models.DateField()
    due_date   = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    def save(self, *args, **kwargs):
        # herda cliente de contract se não informado
        if self.contract and not self.client:
            self.client = self.contract.client
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.contract.code if self.contract else self.client.name})"