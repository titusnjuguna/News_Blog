# Generated by Django 3.2.8 on 2021-11-08 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
