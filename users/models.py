import pycountry
import shortuuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from .validators import validate_phone_number

def generate_short_uuid():
    return shortuuid.ShortUUID().random(length=10)

COUNTRY_CHOICES = [(c.alpha_2, c.name) for c in pycountry.countries]

    
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field is required")
        extra_fields.setdefault("is_active", True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        max_length=10, 
        primary_key=True, 
        default=generate_short_uuid, 
        editable=False, 
        unique=True
    )
    country = models.CharField(max_length=2,choices=COUNTRY_CHOICES)    
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    solde = models.FloatField(default=1000)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def clean(self):
        """ Validate phone number dynamically based on country. """
        if self.country:
            self.phone_number = validate_phone_number(self.phone_number, self.country)

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation before saving
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name} - {self.phone_number}'
