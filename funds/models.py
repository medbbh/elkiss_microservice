from django.db import models
import shortuuid
from elkiss_project import settings

def generate_short_uuid():
    return shortuuid.ShortUUID().random(length=10)

class Fund(models.Model):
    status_choices = [
        ('Open','open'),
        ('Closed','closed')
    ]

    id = models.CharField(
        max_length=10, 
        primary_key=True, 
        default=generate_short_uuid, 
        editable=False, 
        unique=True
    )
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='funds')
    phone_beneficiary = models.IntegerField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    total_participants = models.IntegerField(default=0)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=10, default='open', choices=status_choices)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.owner}'
    
    def add_donation(self, amount):
        """Method to add donations and update current amount."""
        self.current_amount += amount
        self.save()