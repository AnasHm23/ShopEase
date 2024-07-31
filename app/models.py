from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class  EmailAddress(models.Model):
    email = models.EmailField(unique=False)
    is_active = models.BooleanField(default=True)
    
    def clean(self):
        if self.is_active:
            if EmailAddress.objects.filter(email=self.email, is_active=True).exclude(pk=self.pk).exists():
                raise ValidationError({'email': 'Active email addresses must be unique.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
        

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    