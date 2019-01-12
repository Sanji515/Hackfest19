from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import RegexValidator

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_no = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # email = models.EmailField(max_length=70, blank=True)
    city = models.CharField(max_length=100, blank=True)


class Farmers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_id = models.IntegerField(default=0, null=True)
    price = models.IntegerField(default=0, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    crop_mobile_no = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)


class Crop(models.Model):
    crop_id = models.IntegerField(default=0, blank=True)
    farmers = models.ManyToManyField(Farmers, blank=True)


# This is for Profile model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
