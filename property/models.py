from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = 'property/{owner_id}/{title}-{filename}'.format(
        owner_id=str(instance.owner.id), title=str(instance.title), filename=filename)
    return file_path


class PropertyListing(models.Model):

    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    image2 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image3 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image4 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image5 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image6 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image7 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    address = models.CharField(max_length=200, default=False)
    city = models.CharField(max_length=100, default=False)
    area = models.CharField(max_length=100, default=False)
    z = (
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CG', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OD', 'Odisha'),
        ('PB', 'Punjab'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'),
        ('TR', 'Tripura'),
        ('UK', 'Uttrakhand'),
        ('UP', 'Uttar Pradesh'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli'),
        ('DD', 'Daman and Diu'),
        ('DL', 'Delhi'),
        ('LH', 'Ladakh'),
    )

    state = types = models.CharField(max_length=25, choices=z,
                                     null=False, default=False)
    zipcode = models.IntegerField(default=False)
    description = models.TextField(blank=True, default=False)
    price = models.IntegerField(default=False)
    bedrooms = models.IntegerField(default=False)
    latitude = models.FloatField(default='32.1111')
    longitude = models.FloatField(default='32.1111')
    bathrooms = models.IntegerField(default=False)
    sqft = models.IntegerField(default=False)

    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    year_built = models.IntegerField(default=0)
    x = (
        ('R', 'Rent'),
        ('S', 'Sell'),
        ('B', 'Both')
    )
    types = models.CharField(max_length=1, choices=x,
                             null=False, default='R')

    y = (
        ('Y', 'yes'),
        ('N', 'No')
    )
    premium = models.CharField(max_length=1, choices=y,
                               null=False, default='N')

    pool = models.BooleanField()

    parking = models.BooleanField()

    gym = models.BooleanField()

    balcony = models.BooleanField()
    z = (
        ('A', 'Apartment'),
        ('H', 'House')
    )
    stay = models.CharField(max_length=1, choices=z,
                            null=False, default='H')

    k = (
        ('V', 'Verified'),
        ('N', 'Not Verified'),
        ('R', 'rejected')
    )
    Verify = models.CharField(max_length=1, choices=k,
                              null=False, default='N')

    def __str__(self):
        return self.title


@receiver(post_delete, sender=PropertyListing)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.owner.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=PropertyListing)
