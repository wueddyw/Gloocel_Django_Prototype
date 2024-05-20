from django.db import models
from django.contrib.auth.models import User 
from suite.models import Suite
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save 
from django.dispatch import receiver


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length = 50, null = True)
    last_name = models.CharField(max_length = 50, null = True)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField(default='+16044345734', max_length=128, region=None)
    suite = models.ForeignKey(Suite, related_name='Suite', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
