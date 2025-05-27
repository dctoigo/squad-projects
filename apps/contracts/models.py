import hashlib
from datetime import datetime
from django.db import models
from apps.clients_suppliers.models import Party
from apps.manager.models import (
    Technology, ServiceType,
    BillingType, PaymentInterval
)

class Contract(models.Model):
    code = models.CharField('Identifier', max_length=32, unique=True, editable=False)
    client = models.ForeignKey(Party, on_delete=models.PROTECT, related_name='contracts')
    start_date = models.DateField('Start Date')
    due_date   = models.DateField('Due Date', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    billing_type     = models.ForeignKey(
        BillingType, on_delete=models.PROTECT, related_name='+'
    )
    payment_interval = models.ForeignKey(
        PaymentInterval, on_delete=models.PROTECT, related_name='+'
    )

    value = models.DecimalField('Value', max_digits=10, decimal_places=2, default=0)

    technologies  = models.ManyToManyField(Technology, blank=True)
    service_types = models.ManyToManyField(ServiceType, blank=True)
    scope         = models.TextField('Scope')
    milestones    = models.TextField('Milestones', blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            now = datetime.now().isoformat()
            short_hash = hashlib.sha1(now.encode()).hexdigest()[:8]
            self.code = f"CT-{short_hash}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} – {self.client.name}"