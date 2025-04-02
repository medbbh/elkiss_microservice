from django.db import models

from elkiss_project import settings
from funds.models import Fund
import shortuuid

def generate_short_uuid():
    return shortuuid.ShortUUID().random(length=10)

class Transaction(models.Model):
    id = models.CharField(
        max_length=10, 
        primary_key=True, 
        default=generate_short_uuid, 
        editable=False, 
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    cagnotte = models.ForeignKey(
        Fund,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: You can store the tax or total paid if needed
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Transaction {self.id} - {self.amount} MRU"