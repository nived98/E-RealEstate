from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
# Create your models here.
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from property.models import PropertyListing
from datetime import datetime
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)


        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    
def __str__(self):
    return f'{self.user.username} UserProfile'

def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    

def create_customer(sender, **kwargs):
    if kwargs['created']:
        user = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_customer, sender=User)


def pre_save_set_fields(sender, instance, *args, **kwargs):

    instance.first_name = instance.user.first_name
    instance.last_name = instance.user.last_name
    instance.email = instance.user.email


pre_save.connect(pre_save_set_fields, sender=UserProfile)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Invoice(models.Model):
    issued_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_purchased = models.ForeignKey(
        PropertyListing, on_delete=models.CASCADE)

    slug = models.CharField(max_length=120, unique=True)
    date = models.DateTimeField(blank=False, default=datetime.now)
    registery = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    final = models.IntegerField(default=0)
    invoice_id = models.IntegerField(default=0)

    def __str__(self):
        return '%d %s' % (self.id, self.slug)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Invoice, self).save(*args, **kwargs)


class BankApi(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_interested = models.ForeignKey(
        PropertyListing, on_delete=models.CASCADE)
    date_queried = models.DateTimeField(
        auto_now_add=True, verbose_name="date queried")

    def __str__(self):
        return '%d' % (self.id)
