# Generated by Django 2.2.6 on 2019-12-13 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_bankapi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_phone',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_zipcode',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default.jpeg', upload_to='profile_pics'),
        ),
    ]
