# Generated by Django 4.0.4 on 2022-05-27 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blog_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.ImageField(upload_to='blogimage'),
        ),
    ]